import os
from io import BytesIO

import boto3
import uuid
from PIL import Image

from flask import jsonify, request, current_app, send_file
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from api import db
from api.model import Cat
from api.model.pedigree import Pedigree

file_bp = Blueprint('file', __name__, url_prefix='/file')

@file_bp.route('/pedigree',  methods=['POST'])
@jwt_required()
def upload_file():
    user_id =  get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({'status': 'ok',
                        'error_message': 'Lack of parameter',
                        'data': {}}), 400
    file = request.files['file']
    if not verify_uploaded_image(file):
        return jsonify({'status': 'ok',
                        'error_message': 'Illegal parameter',
                        'data': {}}), 400

    # uuidでファイル名を作成
    unique_id = uuid.uuid4().hex
    upload_image_name = str(unique_id) + '.' + os.path.splitext(file.filename)[1].lstrip(".").lower()

    # Supabase storage(s3) connectionを用意
    session = boto3.Session(
        aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
        region_name=current_app.config['S3_REGION']
    )
    s3 = session.client('s3', endpoint_url=current_app.config['S3_ENDPOINT'])
    try:
        s3.put_object(Body=file, Bucket=current_app.config['S3_BUCKET_NAME'], Key='pedigree/' + str(user_id) + '/' + upload_image_name, ContentType=file.content_type)
    except Exception as e:
        print(f"An unexpected upload error occurred: {e}")
        return jsonify({'status': 'ok',
                        'error_message': 'Upload failed',
                        'data': {}}), 500

    cat = Cat(name=None, breed=None, nickname=request.form['nickname'])
    db.session.add(cat)
    db.session.flush()
    pedigree = Pedigree(cat_id=cat.id, upload_user_id=user_id, file_name=upload_image_name)
    db.session.add(pedigree)
    db.session.flush()
    db.session.commit()

    return jsonify({'status': 'ok',
                    'error_message': '',
                    'data': {
                        'pedigree_id': pedigree.id
                    }}), 200

def verify_uploaded_image(file):
    # 拡張子check
    ext = os.path.splitext(file.filename)[1].lstrip(".").lower()
    if ext not in current_app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return False

    # content_type確認
    content_type = file.content_type
    if not content_type.startswith('image/'):
        return False

    # ファイルサイズ確認
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > current_app.config['ALLOWED_MAXIMUM_IMAGE_SIZE']:
        return False
    file.seek(0)

    # 画像であるかどうかを確認
    try:
        with Image.open(file) as img:
            img.verify()
        file.seek(0)
    except Exception as e:
        print(f"An unexpected upload error occurred: {e}")
        return False

    return True

@file_bp.route('/pedigree',  methods=['GET'])
@jwt_required()
def get_file():
    user_id =  get_jwt_identity()
    data = request.json
    pedigree = db.session.query(Pedigree).get(data['pedigree_id'])

    if (pedigree is None) or (not check_file_permission(user_id, pedigree.upload_user_id)):
        return jsonify({'status': 'ok',
                        'error_message': 'Illegal parameter',
                        'data': {}}), 400

    # Supabase storage(s3) connectionを用意
    session = boto3.Session(
        aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
        region_name=current_app.config['S3_REGION']
    )
    s3 = session.client('s3', endpoint_url=current_app.config['S3_ENDPOINT'])
    try:
        response = s3.get_object(Bucket=current_app.config['S3_BUCKET_NAME'],Key='pedigree/' + str(user_id) + '/' + pedigree.file_name)
        file_content = response['Body'].read()
        file_stream = BytesIO(file_content)
        file_stream.seek(0)
        return send_file(
            file_stream,
            download_name=pedigree.file_name,
            mimetype=response['ContentType']
        )
    except Exception as e:
        print(f"An unexpected download error occurred: {e}")
        return jsonify({'status': 'ok',
                        'error_message': 'download failed',
                        'data': {}}), 500

def check_file_permission(user_id, upload_user_id):
    # companyに関するのは考慮しない / 管理者に関するのも考慮しない
    # アップロード者であれば確認できる
    return user_id == upload_user_id

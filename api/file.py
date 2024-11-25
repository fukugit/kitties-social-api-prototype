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
# @jwt_required()
def upload_file():
    # user_id =  get_jwt_identity()
    user_id =  1


    if 'nickname' not in request.form:
        return jsonify({'status': 'ok',
                        'error_message': 'Lack of parameter',
                        'data': {}}), 400
    check_name_result, nickname = verify_nickname(request.form['nickname'])
    if not check_name_result:
        return jsonify({'status': 'ok',
                        'error_message': 'Illegal parameter',
                        'data': {}}), 400

    if 'file' not in request.files or len(request.files.getlist('file')) != 1:
        return jsonify({'status': 'ok',
                        'error_message': 'Lack of parameter',
                        'data': {}}), 400
    file = request.files.getlist('file')[0]
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

    # image upload
    try:
        s3.put_object(Body=file, Bucket=current_app.config['S3_BUCKET_NAME'], Key='pedigree/' + str(user_id) + '/' + upload_image_name, ContentType=file.content_type)
    except Exception as e:
        print(f"An unexpected upload error occurred: {e}")
        return jsonify({'status': 'bad',
                        'error_message': 'Upload failed',
                        'data': {}}), 500

    # Catと血統書recordを追加
    cat = Cat(name=None, breed=None, nickname=nickname)
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

def verify_nickname(nickname):
    nickname = nickname.strip()

    # 長さ制限
    # if len(nickname) > XX

    # 特殊文字
    # if not re.match('XXX', nick_name)

    return True, nickname

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

@file_bp.route('/pedigree/<pedigree_id>',  methods=['GET'])
# @jwt_required()
def get_file(pedigree_id):
    # user_id =  get_jwt_identity()
    user_id =  1

    if (pedigree_id is None) or (not pedigree_id.isdigit()):
        return jsonify({'status': 'ok',
                        'error_message': 'Illegal parameter',
                        'data': {}}), 400
    pedigree = db.session.query(Pedigree).get(pedigree_id)

    if not check_file_permission(user_id, pedigree.upload_user_id):
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
        return jsonify({'status': 'bad',
                        'error_message': 'download failed',
                        'data': {}}), 500

def check_file_permission(user_id, upload_user_id):
    # companyに関するのは考慮しない / 管理者に関するのも考慮しない
    # アップロード者であれば確認できる
    # return user_id == upload_user_id
    return True

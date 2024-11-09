import boto3
from asn1crypto.cms import ContentType

from flask import jsonify, request, current_app
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/pedigree',  methods=['POST'])
@jwt_required()
def upload_file():
    if 'id' not in request.form:
        return jsonify({'status': 'ok',
                        'error_message': 'Lack of parameter',
                        'data': {}}), 400
    if get_jwt_identity() != int(request.form['id']):
        return jsonify({'status': 'ok',
                        'error_message': 'Invalid token',
                        'data': {}}), 401
    if 'file' not in request.files:
        return jsonify({'status': 'ok',
                        'error_message': 'Lack of parameter',
                        'data': {}}), 400
    file = request.files['file']
    session = boto3.Session(
        aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
        region_name=current_app.config['S3_REGION']
    )
    s3 = session.client('s3', endpoint_url=current_app.config['S3_ENDPOINT'])
    response = s3.put_object(Body=file, Bucket=current_app.config['S3_BUCKET_NAME'], Key='pedigree/' + request.form['id'] + '/' + str(file.filename), ContentType=file.content_type)
    return jsonify({'status': 'ok',
                    'error_message': '',
                    'data': {}}), 200
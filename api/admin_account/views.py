from flask_restx import Resource,fields,Namespace
from ..admin_account.admin_model import AdminAccount
from ..models.patients_model import Patient
from ..models.doctors_model import Doctor
#from ..models.cabinet_model import Cabinet
from ..models.music_model import Musique
from ..models.categorie_model import Category
from ..models.admin_token import AdminToken
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_refresh_token,create_access_token,jwt_required,get_jwt_identity
from flask import  abort,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from http import HTTPStatus
from datetime import datetime,timedelta

"""
views for Admin views CRUD for Admin Account ,add doctor , manage other endpoint
"""

admin_view=Namespace("admin",description="Endpoint for compte admin ")




#---------------- sign up ------------------

register_model=admin_view.model(
    "register_admin",{
        "username":fields.String(required=True),
        "first_name":fields.String(required=True),
        "last_name":fields.String(),
        "email":fields.String(required=True),
        "password":fields.String()
    }
)
register_response=admin_view.model(
    "response admin",{
        "message":fields.String(),
        
    }
)
@admin_view.route("/auth/signup")
class SignUpAdmin(Resource):
    @admin_view.expect()
    def post(self):
        data=request.get_json()
        filter=AdminAccount.query.filter_by(username=data.get("username")).first()
        filter_1=AdminAccount.query.filter_by(email=data.get("email")).first()
        if filter is not None:
            return abort(401,"username already exist")
        if filter_1 is not None:
            return abort(401,"email already exist")
        user:AdminAccount=AdminAccount(
        username=data.get("username"),
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        password=generate_password_hash(data.get("password")),
         urlimage="",)
        response= {
         "status_code":HTTPStatus.CREATED,
         "message":"Admin account created with succes "
         }
        return response
    
#------------------ login --------------------
login_model=admin_view.model(
    "login_request",{
        "email":fields.String(required=True),
        "password":fields.String(required=True)
    }
)
login_response=admin_view.model(
    "login_response",{
        "status_code":fields.Integer(),
        "session":fields.Boolean(),
        "access_token":fields.String(),
        "refresh_token":fields.String(),
        "expire_in":fields.DateTime()
    }
)

@admin_view.route("/auth/login")
class LoginAmin(Resource):
    @admin_view.expect(login_model)
    @admin_view.marshal_with(login_response)
    def post(self):
     data=request.get_json()
     email=data.get("email")
     password=data.get("password")
     user :AdminAccount=AdminAccount.query.filter_by(email=email).first()
     if user is not None and check_password_hash(user.password,password):
         token =AdminToken.query.filter_by(patient_id=user.id).first()
         access_token=create_access_token(identity=user.username)
         refresh_token=create_refresh_token(identity=user.username)
         expire =  datetime.utcnow()
         expire +=  timedelta(hours=23)
         if token is None:
             token=AdminToken(
                 access_token=access_token,
                 refresh_token=refresh_token,
                 patient_id=user.id,
                 expired_in=expire)
             token.save()
         else:
             token.access_token=access_token
             token.refresh_token=refresh_token
             token.expired_in=expire
             token.update()
         result={
             "status_code":HTTPStatus.OK,
             "access_token":access_token,
             "refresh_token":refresh_token,
             "session":True,
             "expire_in":token.expired_in
         }
         return result
     return abort(HTTPStatus.NOT_FOUND,"verifie your email or password wrong")


@admin_view.route("/auth/reset_password")
class ResetPassword(Resource):
    def post(self):
        pass

@admin_view.route("/auth/refresh-token")
class RefreshToken(Resource):
    def Post(self):
        pass

@admin_view.route("/auth/me")
class FetchAdmin(Resource):
    def post(self):
        pass
    
@admin_view.route("/doctors")
class Doctors(Resource):
    def get(self):
        pass
    def post(self):
        pass

@admin_view.route("/doctor/<int:id>")
class DoctorByid(Resource):
    def get(self,id):
        pass
    def put(self,id):
        pass 
    def delete(self,id):
        pass 

@admin_view.route("/doctor/<name>")
class DoctorByName(Resource):
    def get(self,name):
        pass
    def put(self,name):
        pass 
    def delete(self,name):
        pass 


##################### musique #############################
musique_model=admin_view.model(
    "categorie_model",{
        "title":fields.String(required=True),
        #"songer":fields.String(required=True),
        "url":fields.String(required=True)
        
    }
)

@admin_view.route("/musique")
class MusiqueUpload(Resource):
    @admin_view.expect()
    def post(self):
        data=request.get_json()
        username=get_jwt_identity()
        admin:AdminAccount=AdminAccount.query.filter_by(username=username).first()
        if data.get("title")is None:
            return abort(404, "Music title is empty")
        if data.get("url")is None:
            return abort(404, "Music title is empty")
        
    

##################### category #############################
categorie_model=admin_view.model(
    "categorie_model",{
        "name":fields.String(required=True),
        "image":fields.String(required=True),
    }
) 

@admin_view.route("/categorie")
class CategorieUpload(Resource):
    @admin_view.expect()
    def post(self):
        data=request.get_json()
        username=get_jwt_identity()
        admin:AdminAccount=AdminAccount.query.filter_by(username=username).first()
        if data.get("name") is None :
            return abort(404,"job_occuped is empty")
        if data.get("image_url") is None :
            return abort(404,"society is empty")
        categorie:Category=Category(
            name=data.get("name"),
            image_url=data.get("image_url")
            #admin_id=admin.id
        )
        categorie.save()
        return categorie
        
##################### category #############################



''' username=get_jwt_identity()
        doctor:Doctor=Doctor.query.filter_by(username=username).first()
        data=request.get_json()
        if data.get("cabinet_address") is None :
            return abort(404,"cabinet_address is empty")
        if data.get("cabinet_contact") is None :
            return abort(404,"cabinet_contact is empty")
        if data.get("time_openning") is None :
            return abort(404,"time_openning is empty")
        if data.get("time_closing") is None :
            return abort(404,"time_closing is empty")
        cabinet_address=data.get("cabinet_address")
        cabinet_contact=data.get("cabinet_contact")
        time_opning=data.get("time_openning")
        time_closed=data.get("time_closing")
        cabinet:Cabinet=Cabinet(
            cabinet_address=cabinet_address,
            cabinet_contact=cabinet_contact,
            time_opning=time_opning,
            time_closed=time_closed,
            doctor_id=doctor.id
        )
        cabinet.save()
        return jsonify(message="cabinet add with succes")
'''


@admin_view.route("/patients")
class FetchAllPatient(Resource):
    def get(self):
        pass

@admin_view.route("/patient/id")
class FetchAllPatient(Resource):
    def get(self,id):
        pass
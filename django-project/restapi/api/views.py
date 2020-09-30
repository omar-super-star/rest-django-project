from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import users
from .serializers import userstojson
userused=None
firstsign=True
sign=None
print("start from first")
class userslist(APIView):
    def get(self,request):
        user=users.objects.all()
        seri=userstojson(user,many=True)
        return Response(seri.data)
    def post(self,request):
        global sign,firstsign,userused

        print(sign)
        print(firstsign)
        req=dict(request.data)
        found_email=False
        true_user_id=False
        true_password=False
        userlist=list(users.objects.all())
        print(userlist)
        email=req.get("email",None)
        user_id=req.get("user_id",None)
        password=req.get("password",None)
        firstname = req.get("firstname", None)
        lastname=req.get("lastname",None)

        if firstsign:
            if email != None :

                for i in userlist:

                    if email[0] == i.email:
                        userused=i
                        found_email = True
            if found_email == False:
                sign=False
                firstsign = False
                return Response({
                    "userid":"not registered",
                    "login_type": "signup",

                })
            else:
                sign=True
                firstsign = False
                return Response({
                    "userid": userused.id,
                    "login_type": "signin",
                })

        elif sign ==True:

            print(userused.password)
            print(userused.id)
            print(user_id)
            if user_id[0] == str(userused.id) and check_password(password[0],userused.password):
                return Response({
                    "message": "login successful"
                })
            else:
                return Response({
                    "message": "failed"
                })
        else:
            if password != None and email != None and firstname != None and lastname != None:

                user=users(email=email[0],
                       password=make_password(password[0]),
                       firstname=firstname[0],
                       lastname=lastname[0],
                       favorite=None)
                user.save()
            firstsign=True
        return Response(request.data)
class details(APIView):
    def get(self,request,user_id):
        try:
            resend_data=users.objects.filter(id=user_id).first()
        except Exception as e:
            return Response({
                "error": e
            })
        fav=resend_data.favorite
        if fav != None:
            fav=fav.split(",")
        return Response({
            "email":resend_data.email,
            "firstname":resend_data.firstname,
            "lastname":resend_data.lastname,
            "favorite":fav
        })

class add_fav(APIView):
    def put(self,request):
        data=dict(request.data)
        user_id=data.get("user_id",None)
        fav=data.get("favorite",None)
        if user_id == None or fav ==None:
            return Response({
                "error":"please send the user_id and fav"
            })
        try:
                 user_data = users.objects.filter(id=int(user_id[0])).first()
        except Exception as e:
            return Response({
                "error": e
            })
        fav_user=user_data.favorite
        if fav_user == None or fav_user=="":
            user_data.favorite=fav[0]+","
        else:
            user_data.favorite=user_data.favorite+fav[0]+","
        user_data.save()
        return Response({
            "success":True
        })
class remove(APIView):
    def delete(self,request):
        data=dict(request.data)
        user_id=data.get("user_id",None)
        fav=data.get("favorite",None)
        if user_id == None or fav ==None:
            return Response({
                "error":"please send the user_id and fav"
            })
        user_data = users.objects.filter(id=int(user_id[0])).first()
        fav_user=user_data.favorite
        if fav_user == None or fav[0] not in fav_user:
            return Response({
                "error":"that favorite is not found"
            })
        else:
            first=fav_user.find(fav[0])
            end=first+len(fav[0])
            final_fav=fav_user[:first]+fav_user[end:]
            user_data.favorite=final_fav
        user_data.save()
        return Response({
            "success":True
        })
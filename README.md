You will need to install:
	
	    -Django: pip install django
	    -Pillow: pip install pillow
	    -Crispy-Forms: pip install django-crispy-forms
	
	
If you want the recovery password feature to work you have to go to settings.py and change:
	
		-EMAIL_HOST_USER = "YOUR GMAIL ACCOUNT"
		-EMAIL_HOST_PASSWORD = "YOUR PASSWORD"
	
Also, you will need to allow your Gmail account to be accessed by less secure apps.

# Summery
web app n kun application garaagaraa sadii kan of keessaa qabu yoo ta'u, its main use is a degital procurement/ e-procurement. Kan inni ittiin hojjetames django frame work dhaani. 

## E-procurement
is a digital procurement methodology implimented in this web app. Its main features are an advanced filtering of the active requests from the business owner endpoints, filtering the lowest bid price after the expiration of the request(from the admin endpoint), the requestion can be imported after preparing in excel format, a business owner can print its proforma(after submitting the proforma) and more. 

## Endpoints
'' - Landing-Page
'about/' - About-Page
'admin/' - Admin Access endpoint "Where admin creates, deletes, and updates - The requestion, Blog, Project and initiatives, Category, subcategory, regions and others "
'register/'
'login/',
'logout/'
'password-reset/' 
'password-reset/done/'
'password-reset-confirm/<uidb64>/<token>/'
'password-reset-complete/'
'profile/'
'blog/'
'blog/<int:pk>/'
'projects/'
'projects/<pk>/'
'usernotifications/'
'notifications/'
'requestion/'
'requestion/<pk>/'
'requestion/<pk>/expired'
'requestion/<pk>/filled'
'requestion/print/<int:pk>/'
'requestion/<pk>/fill/'
'business/new'
'business/<pk>/'
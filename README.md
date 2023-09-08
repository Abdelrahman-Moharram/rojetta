# apps
## accounts 


### Views

### Profile
- name
- phone
- image
- doctors show thier data certificates 
- specialzation
- diplomas
- rates
- when clinic will open and will close 
- holidays
- user can book an appointment with the doctor even if the clinic is closed to book in the earliest available appointment


#### Registeration & Login
- register as doctor or as patient  
- make it with forms.py as a practice 
- make error message for each field 
- add custom validation for password in registeration
- make user login with email or username or phonenumber

### Models

#### Custom user model
- User
    - fname
    - lname
    - email
    - date_joined
    - is_staff
    - username
    - phonenumber

- Doctor
    - image
    - government => FK
    - state => FK
    - detailLocation
    - latitude
    - longitude
    - coverletter
    - bio
    - price 
- Specialization
    - name
    - faculty
    - university
- Patient
    - government
    - state
    - detailLocation

- government
    - name

- state
    - name

SkillType
- name

Skill (like certificates and diplomas, and experience)

- name
- SkillType
- from (date)
- to (date)
- file (optional)
#### additional

- different privillages for each
    - django groups (to study)

- try to integrate location with google maps


---
## Home

### views
#### home

- find doctor based on the location, specialization, rate and price


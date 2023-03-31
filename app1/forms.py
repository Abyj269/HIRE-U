
# from cProfile import label
from django import forms
# from app1.models import Profile


GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ]

SKILL_CHOICES =[
    ('Effective communication', 'Effective communication'),
    ('Teamwork','Teamwork'),
    ('Creativity','Creativity'),
    ('Problem-solving','Problem-solving'),
    ('Leadership','Leadership'),
    ('Time management','Time management'),
    ('Critical thinking','Critical thinking'),
    ('Data analysis','Data analysis'),
    ('Web analytics','Web analytics' ),
    ('Email marketing','Email marketing'),
    ('Web scraping','Web scraping'),
    ('CRO and A/B Testing','CRO and A/B Testing'),
    ('Data visualization','Data visualization'),
    ('Search Engine and Keyword Optimization','Search Engine and Keyword Optimization'),
    ('Adobe Creative Suite','Adobe Creative Suite'),
    ('Infographics','Infographics'),
    ('Research and data analysis','Research and data analysis'),
    ('Technical writing','Technical writing'),
    ('Cloud networking and file sharing','Cloud networking and file sharing'),
    ('Microsoft Excel','Microsoft Excel'),
    ('Big Data Analysis & SQL','Big Data Analysis & SQL'),
    ('Accounting Software','Accounting Software'),
    ('Research & Data analysis','Research & Data analysis'),
    ('HTML/CSS','HTML/CSS'),
    ('Javascript','Javascript'),
    ('Wordpress','Wordpress'),
    ('Search Engine Optimization (SEO)','Search Engine Optimization (SEO)'),
    ('Adobe Photoshop', 'Adobe Photoshop'),
    ('Testing/Debugging','Testing/Debugging'),
    ('Data Mapping','Data Mapping'),
    ('Agile Business Analysis','Agile Business Analysis'),
    ('Machine learning','Machine learning') ,
    ('Python', 'Python'),
    ('Django', 'Django'),
    ('Web Development', 'Web Development'),
    ('Database', 'Database'),
    ('SQL', 'SQL')
]

class ProfileForm(forms.ModelForm):  #creating form for profile 
    gender = forms.ChoiceField(choices = GENDER_CHOICES, widget=forms.RadioSelect)
    skills = forms.MultipleChoiceField(choices=SKILL_CHOICES)
    class Meta:
        # model= Profile
        fields = ['name','address','email', 'social', 'number', 'title', 'objective', 'company_name','job_title', 'job_works', 'job_date_from','job_date_to', 'college_name','course', 'course_modules', 'gpa','skills', 'profile_picture']
        labels = {
            'number': 'Contact ',
            'social': 'Social (eg: linkedin) / Optional ',
            'company_name': 'Experience (Company Name & Address) ',
            'job_title': 'Job Title ',
            'job_works': 'Job Summary ',
            'job_date_form': 'Started From ',
            'job_date_to' : 'To ',
            'college_name' : 'College Name & Address ',
            'course_module': 'Course Modules ',
            'gpa':'GPA ',
            'profile_picture' : 'Profile Picture '
            } #changes label of form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'social': forms.URLInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'objective': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_works': forms.TextInput(attrs={'class': 'form-control'}),
            'job_date_from': forms.DateInput(attrs={'class': 'form-control', 'id':'datepickerfrom'}),
            'job_date_to': forms.DateInput(attrs={'class': 'form-control', 'id':'datepickerto'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'course_modules': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control'})
        }
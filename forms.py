from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField
from wtforms.validators import Required, Length
from models import User
    
class EditProfileForm(Form):
    name = TextField('name', validators = [Required()])
    email = TextField('email')
    phone = TextField('phone')
    
    def __init__(self, original_name, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_name = original_name
        
    def validate(self):
        if not Form.validate(self):
            return False
        if self.name.data == self.original_name:
            return True
        user = db_session.query(User).filter_by(name = self.name.data).first()
        if user != None:
            self.name.errors.append('This user name is already in use. Please choose another one.')
            return False
        return True
        
        

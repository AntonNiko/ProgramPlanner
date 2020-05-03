from djongo import models 

class Program(models.Model):
    institution = models.CharField(
        max_length = 50,
        choices = [
            ('university_of_victoria', 'university_of_victoria')
        ]
    )
    name = models.CharField(max_length = 50)
    requirements = models.DictField(default={'expressions':{}}, blank=False)

    def to_dict(self):
        result = {
            'institution': self.institution,
            'name': self.name,
            'requirements': self.requirements
        }
        return result
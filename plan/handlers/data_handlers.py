
class DataHandler():

    @staticmethod
    def get_course_data(request):
        """
        Returns a list of courses corresponding to request parameters 
        provided.
        """

        subject = request.GET.get('subject', None)
        subjects_only = request.GET.get('subjects_only', None)
        number = request.GET.get('number', None)
        numders_only = request.GET.get('numbers_only', None)
        number_min = request.GET.get('number_min', None)
        number_max = request.GET.get('number_max', None)
        
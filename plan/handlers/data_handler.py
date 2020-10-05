#  Copyright (c) 2020. by Anton Nikitenko
#  All rights reserved.

from plan.models import Course, Program


class DataHandler:
    RESPONSE_BASE = {'success': False, 'message': '', 'data': None}

    @staticmethod
    def get_course_data(request):
        """
        Returns a list of courses corresponding to request parameters 
        provided.

        The following parameters specified by the `request` are supported:
          - 'subject': If set, the result shall only contain courses for that subject
          - 'number': If set, the result shall only contain courses that match the number
        
        If 'subject' is undefined, all of the institution's courses will be returned.
        If 'subject' is defined and 'number' undefined, then all courses for that subject will be returned.

        Args:
          - request: An `HttpRequest` object.
        Returns:
          - response: A JSON-serializable object with result.
        """
        response = DataHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        subject = request.GET.get('subject', None)
        number = request.GET.get('number', None)

        if subject is None and number is None:
            response['data'] = [course.to_dict() for course in Course.objects.all()]
            response['success'] = True

        elif subject is not None and number is None:
            response['data'] = [course.to_dict() for course in Course.objects.filter(course_code__exact={'subject': subject})]
            response['success'] = True

        elif subject is not None and number is not None:
            response['data'] = [course.to_dict() for course in
                      Course.objects.filter(course_code__exact={'subject': subject}).filter(
                          course_code__exact={'number': number})]
            response['success'] = True

        # Invalid request parameters
        else:
            response['message'] = 'Invalid request parameter values'

        return response

    @staticmethod
    def get_program_data(request):
        """
        Returns a list of programs as specified by the request parameters provided.

        Args:
          - request: An `HttpRequest` object.
        Returns:
          - response: A JSON-serializable object with result.
        """
        response = DataHandler.RESPONSE_BASE.copy()

        # Parameter parsing
        institution = request.GET.get('institution', None)
        name = request.GET.get('name', None)
        assert institution is not None

        if name is None:
            response['data'] = [program.to_dict() for program in Program.objects.filter(institution=institution)]
            response['success'] = True
        else:
            response['data'] = Program.objects.filter(institution=institution).filter(name=name)[0]
            response['success'] = True

        return response

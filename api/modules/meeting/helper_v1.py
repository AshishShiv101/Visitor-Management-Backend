from datetime import datetime
from api.utils.response import ApiResponse
from api.utils.validation import ValidationHelper
import api.utils.http_status as status
from db.base import db
from db.models.users_model import Users
from db.models.visitors_model import Visitors
from db.models.meetings_model import Meetings
from db.models.meting_status_model import MeetingStatus
from db.utils.db_enums import MeetingsStatusEnum

class MeetingHelper:

    def __init__(self):
        self.response_helper = ApiResponse()
        self.validation_helper = ValidationHelper()
    
    def initialize_resource_action_map(self, request_type : str):
        resource_action_map = None

        if request_type == "get":
            resource_action_map = {
                "get_meetings" : self.get_meetings,
                "get_specific_meeting" : self.get_specific_meeting
            }
        elif request_type == "post":
            resource_action_map = {
                "schedule_meeting": self.schedule_meeting,
            }
        elif request_type == "patch":
            resource_action_map = {
                "update_meeting_status": self.update_meeting_status,
            }
        return resource_action_map
    
    def validate_action(self, request_params : dict, request_map : dict):
        return request_params.get("_action") in request_map.keys()
    
    def format_meetings_details(self, meetings_details : list) -> list:
        formatted_meetings_details = []

        for meeting in meetings_details:
            meeting_details = {}
            user_details = Users.query.filter_by(id = meeting.user_id).first()
            meeting_details['user'] = user_details.user_name

            visitor_details = Visitors.query.filter_by(id = meeting.visitor_id).first()
            meeting_details['visitor_name'] = visitor_details.visitor_name
            
            meeting_details['meeting_time'] = meeting.meeting_time.strftime('%Y-%m-%dT%H:%M:%S')
            meeting_details['meeting_remarks'] = meeting.meeting_remarks

            meeting_status_details = MeetingStatus.query.filter_by(id = meeting.meeting_status_id).first()
            meeting_details['meeting_status'] = meeting_status_details.meeting_status.value

            print(formatted_meetings_details)
            formatted_meetings_details.append(meeting_details)
        
        return formatted_meetings_details

    def get_meetings_till_date(self, request_params : dict):
        meetings_details : list = []
        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['person_to_meet_name']).get("verification_res") == True:
            user_existence_res = Users.query.filter_by(user_name = request_params.get("person_to_meet_name")).first()
            if not user_existence_res:
                return self.response_helper.response( code = status.HTTP_200_OK, message = "User with this name does not exist", resp_code = 1001)
            
            meetings_details = Meetings.query.filter(Meetings.user_id == user_existence_res.id, Meetings.meeting_time <= request_params["meetings_till_date"]).all() # need to update with paginated requests!
        else:
            meetings_details = Meetings.query.filter(Meetings.meeting_time <= request_params["meetings_till_date"]).all() # need to update with paginated requests!
        
        formatted_meetings_details = self.format_meetings_details(meetings_details = meetings_details)
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Meetings retreived", data = formatted_meetings_details, resp_code = 2000)
    
    def get_all_meetings(self, request_params : dict):

        meetings_details : list = []
        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['person_to_meet_name']).get("verification_res") == True:
            user_existence_res = Users.query.filter_by(user_name = request_params.get("person_to_meet_name")).first()
            if not user_existence_res:
                return self.response_helper.response( code = status.HTTP_200_OK, message = "User with this name does not exist", resp_code = 1001)
            
            meetings_details = Meetings.query.filter_by(user_id = user_existence_res.id).all() # need to update with paginated requests!
        else:
            meetings_details = Meetings.query.all() # need to update with paginated requests!
        
        formatted_meetings_details = self.format_meetings_details(meetings_details = meetings_details)
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Meetings retreived", data = formatted_meetings_details, resp_code = 2000)

    def get_meetings(self, request_params : dict):
        
        if self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ["meetings_till_date"]).get("verification_res") == False:
            return self.get_all_meetings(request_params = request_params)

        return self.get_meetings_till_date(request_params = request_params)
    
    def schedule_meeting(self, request_params : dict):

        param_verification_res = self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ["visitor_name", "person_to_meet_name", "visitor_phno", "visitor_email", "meeting_time"])

        if param_verification_res.get("verification_res") == False:
            return self.response_helper.response( code = status.HTTP_200_OK, message = f"Insufficient details, can't schedule meeting", data = {"missing_params" : param_verification_res.get("missing_params")}, resp_code = 1001)

        user_existence_res = Users.query.filter_by(user_name = request_params.get("person_to_meet_name")).first()

        if not user_existence_res:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User with this name does not exist", resp_code = 1001)

        if not user_existence_res.role_id:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User does not have a role, can't schedule meeting", resp_code = 1001)
        
        visitor_details = None
        existing_visitor = Visitors.query.filter_by(phno = request_params.get("visitor_phno")).first()

        if not existing_visitor:
            visitor_details = Visitors(visitor_name = request_params.get("visitor_name"), phno = request_params.get("visitor_phno"), email = request_params.get("visitor_email"))
            db.session.add(visitor_details)
            db.session.flush()
        else:
            visitor_details = existing_visitor # don't need the updated_at below so doesn't matter if its updated after assigning here...
            setattr(existing_visitor, "updated_at", datetime.now())
            db.session.add(visitor_details)
        
        #validate this data before making entry
        meeting_details = Meetings(visitor_id = visitor_details.id, user_id = user_existence_res.id, meeting_remarks = request_params.get('meeting_remarks', None), meeting_time = request_params.get('meeting_time'))
        db.session.add(meeting_details)
        db.session.commit()

        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Meeting scheduled successfully", resp_code = 2000)
    
    def get_specific_meeting(self, request_params : dict):
        
        param_verification_res = self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['user_name', 'meeting_time'])
        if param_verification_res.get('verification_res') == False:
            return self.response_helper.response( code = status.HTTP_200_OK, message = f"Insufficient details, can't get meeting details", data = {"missing_params" : param_verification_res.get("missing_params")}, resp_code = 1001)
        
        existing_user_res = Users.query.filter_by(user_name = request_params.get("user_name")).first()

        if not existing_user_res:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User with this name does not exist", resp_code = 1001)

        meeting_details = Meetings.query.filter(Meetings.user_id == existing_user_res.id, Meetings.meeting_time == request_params["meeting_time"]).first()
        formatted_meetings_details = []

        if meeting_details:
            formatted_meetings_details = self.format_meetings_details(meetings_details = [meeting_details])
        
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Meeting retreived", data = formatted_meetings_details, resp_code = 2000)

    def update_meeting_status(self, request_params : dict):

        param_verification_res = self.validation_helper.verify_params_existence(request_params = request_params, params_to_verify = ['user_name', 'meeting_time', 'meeting_status'])
        if param_verification_res.get('verification_res') == False:
            return self.response_helper.response( code = status.HTTP_200_OK, message = f"Insufficient details, can't schedule meeting", data = {"missing_params" : param_verification_res.get("missing_params")}, resp_code = 1001)
        
        existing_user_res = Users.query.filter_by(user_name = request_params.get("user_name")).first()

        if not existing_user_res:
            return self.response_helper.response( code = status.HTTP_200_OK, message = "User with this name does not exist", resp_code = 1001)
        
        if request_params.get('meeting_status') not in MeetingsStatusEnum.__members__:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Provided meeting status does not exist!", resp_code = 1001)
        
        meeting_status_details = MeetingStatus.query.filter_by(meeting_status = request_params.get('meeting_status')).first()

        if not meeting_status_details:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f'Provided meeting status exists in enum but not in db', resp_code = 1001)

        meeting_details = Meetings.query.filter(Meetings.user_id == existing_user_res.id, Meetings.meeting_time == request_params["meeting_time"]).first()

        if not meeting_details:
            return self.response_helper.response(code = status.HTTP_200_OK, message = f"Provided meeting does not exist", resp_code = 1001)
        
        setattr(meeting_details, "meeting_status_id", meeting_status_details.id)
        db.session.commit()
        return self.response_helper.response(code = status.HTTP_200_OK, message = f"Meeting status updated successfully", resp_code = 2000)
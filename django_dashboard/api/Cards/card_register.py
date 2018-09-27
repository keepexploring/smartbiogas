# import all the templates you want to use here
from unassigned_pending_jobs import UnassignedPendingJobs


# provide a list of the templates you want regsitered
registered_templates = [UnassignedPendingJobs]
                        

                    
def register_templates(uob):
    [template().build_template() for template in registered_templates]
    
        

def update_cards(uob, perm, company):
    [template().update_card(uob, perm, company) for template in registered_templates]
'''
The purpose of this script is to delete already present objects in the DT platform in order to perform the tests with Self Onboarding Portal
'''

import requests
import os
from pypac import PACSession

# Proxy PAC config
session = PACSession(pac_file_url='http://proxy.tepenet/opl.pac') # OPL Proxy PAC - can be ignored if proxy is not required

# DT API access
dt_base_url = "https://sbomanalyzer.di-secgov.tech.orange/api/v1"
dt_api_key = os.getenv("DT_API_KEY")
dt_headers = {
  'X-Api-Key': dt_api_key
}

# Gitlab API access
gitlab_base_url = "https://gitlab.tech.orange/api/v4"
gitlab_api_key = os.getenv("GITLAB_API_TOKEN")
gitlab_headers = {
    "PRIVATE-TOKEN": gitlab_api_key
}

# 1. Delete OIDC group
def delete_oidc_group():
    # Retrieve diod/secgoc/vkys3350 UUID
    oidc_group = "diod/secgov/vkys3350"
    oidc_get_url = dt_base_url + "/oidc/group"
    response = session.get(oidc_get_url, headers=dt_headers)
    oidc_groups = response.json()
    uuid = None
    #print(oidc_groups)
    for group in oidc_groups:
      if group.get('name') == oidc_group:
          # print(group['name'])
          # print(group['uuid'])
          uuid = group['uuid']
    # Delete OIDC group using retrieved UUID
    if not uuid:
        print("OIDC group does not exist")
        return None
    else:
        oidc_delete_url = oidc_get_url + f"/{uuid}"
       # print(delete_url)
        print ("OIDC group is going to be removed")
        deletion = session.delete(oidc_delete_url, headers=dt_headers)
        print (deletion)


# 2. Retrieve projects to be deleted
def retrieve_gitlab_projects():
    # Retrieve ID of the user 
    get_user_url = gitlab_base_url + "/user"
    # print (get_user_url)
    user_response = session.get(get_user_url, headers=gitlab_headers)
    user_details = user_response.json()
    if user_details.get('id'):
      user_id = user_details['id']
      # print (user_id)
    else: 
      print ("Error: User ID not found")
    # Retrieve contributed projects    
    contributed_projects_url = gitlab_base_url + f"/users/{user_id}/contributed_projects"
    projects_response = session.get(contributed_projects_url, headers=gitlab_headers)
    projects_details = projects_response.json()
    # print(projects_details.text)
    project_list=[]
    for project in projects_details:
        if 'path_with_namespace' in project:
            project_list.append(project['path_with_namespace'])
        else: 
            print ('Error - path of the project not found')
    # print (f"Found {len(project_list)} projects")
    # print(project_list)
    return project_list

# 3. Delete projects 
def delete_projects():
    projects_to_delete_uuid = []
    # projects_to_delete_name = []
    gitlab_project_list = retrieve_gitlab_projects()

    # Retrieve list of current projects 
    project_get_url = dt_base_url + "/project"
    projects_response = session.get(project_get_url, headers=dt_headers)
    #print (projects_response.text)
    projects_details = projects_response.json()
    for gitlab_project in gitlab_project_list:
      for dt_project in projects_details:
        if dt_project.get('name') == gitlab_project:
            projects_to_delete_uuid.append(dt_project['uuid'])
            # projects_to_delete_name.append(dt_project['name'])
    print (f"{len(projects_to_delete_uuid)} projects to be deleted")
    print (projects_to_delete_uuid)
    # print (projects_to_delete_name)
    # for project in project_list:
    if not projects_to_delete_uuid:
       deletion = "No Gitlab projects present in DT"  

    for uuid in projects_to_delete_uuid:
        project_delete_url = project_get_url + f"/{uuid}"
        deletion = session.delete(project_delete_url, headers=dt_headers)
        print (deletion)
    return deletion
 #   projects = ...
def main():
      delete_oidc_group()
      delete_projects()

      
      
if __name__ == "__main__":
    # delete_oidc_group()
    # retrieve_gitlab_projects()
    # delete_projects()
    main()
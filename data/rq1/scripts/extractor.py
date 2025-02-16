from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import json, os, csv
import pandas as pd
from pathlib import Path
from github import Github


repo_list = ['https://github.com/soot-oss/soot.git',
             'https://github.com/wala/WALA.git',
             'https://github.com/plast-lab/doop-mirror.git',
             'https://github.com/opalj/opal',
             'https://github.com/secure-software-engineering/FlowDroid.git',
             'https://github.com/MIT-PAC/droidsafe-src.git',
             'https://github.com/arguslab/Argus-SAF.git',
             'https://github.com/cs-au-dk/TAJS.git',
             'https://github.com/vitsalis/PyCG.git',
             'https://github.com/scottrogowski/code2flow.git',
             'https://github.com/facebook/infer']

tool_list = ['Soot',
             'Wala',
             'Doop',
             'opal',
             'FlowDroid',
             'DroidSafe',
             'AmanDroid',
             'TAJS',
             'PyCG',
             'Code2flow',
             'Infer']

word_list = ['concurrent',
             'concurrency',
             'deterministic',
             'determinism',
             'flaky',
             'flakiness']


def get_issues(repo, tool, dbname): 
      collection_issue = dbname[f'{tool}_issues']
      issues = repo.get_issues(state="all")
      items_issues = []
      for iss in issues:
         iss_dict = {"id": iss.number, 
                     "title": iss.title,
                     "body": iss.body,
                     "state": iss.state,
                     "comments": [_.body for _ in iss.get_comments()]}
         print(iss_dict)
         items_issues.append(iss_dict)
   
      if len(items_issues) > 0:
         collection_issue.insert_many(items_issues)
      else:
         print(f'{tool} has 0 issue.')


def get_commits(repo, tool, dbname): 
   collection_commit = dbname[f'{tool}_commits']
   commits = repo.get_commits()
   items_commits = []
   for com in commits:
      com_dict = {"sha": com.commit.sha, 
                  "author": com.commit.author.name,
                  "message": com.commit.message}
      items_commits.append(com_dict)
   
      print(com_dict)
   if len(items_commits) > 0:
      collection_commit.insert_many(items_commits)
   else:
      print(f'{tool} has 0 commit.')


def search_for_key_issues(search_key, tool):
   collection = dbname[f'{tool}_issues']
   documents = list(collection.find({"$or": [{'title': {"$regex": search_key}},
                                             {'body': {"$regex": search_key}},
                                             {'comments': {"$regex": search_key}}]}))

   Path(f'./results/{search_key}').mkdir(exist_ok=True, parents=True)
   docs = pd.DataFrame(documents)
   docs.to_csv(f'./results/{search_key}/{tool}_issues.csv', index=False)


def search_for_key_commits(search_key, tool):
   collection = dbname[f'{tool}_commits']
   documents = list(collection.find({'message': {"$regex": search_key}}))

   Path(f'./results/{search_key}').mkdir(exist_ok=True, parents=True)
   docs = pd.DataFrame(documents)
   docs.to_csv(f'./results/{search_key}/{tool}_commits.csv', ',', index=False)
      

def get_database():
 
   # Provide the mongodb atlas url to connect to mongodb database.
   CONNECTION_STRING = os.environ['DB_CONNECTION_STRING']
 
   # Create a connection using MongoClient. 
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our project.
   return client['NdGit']

if __name__ == "__main__":  
   
   for i, repo in enumerate(repo_list):

      g = Github(os.environ['GH_TOKEN'])
      user_str, repo_str = repo.replace(".git", "").replace("https://github.com/", "").split("/")
      user = g.get_user(user_str)
      repo = user.get_repo(repo_str)
      
      dbname = get_database()
      get_issues(repo, tool_list[i], dbname)
      get_commits(repo, tool_list[i], dbname)
      
      for key in word_list:
         search_for_key_issues(key, tool_list[i])
         search_for_key_commits(key, tool_list[i])



      



      


   
  
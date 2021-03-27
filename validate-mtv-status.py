import sys, getopt
from jira import JIRA

def validate():
    jira = JIRA(options={'server':"https://deljira/",'verify':"C:/Jiten/personal/software/python/test/deljira-root.cer"},basic_auth=('jitenp','Globe@CES21'))        
    release = jira.issue('GLOB-5128')    
    issueList = release.raw['fields']['issuelinks']
    f = open('MTV-with-not-accepted-US.txt','w')    
    for issue in issueList:
        try:
            print("Scanning MTV -> ",issue['outwardIssue']['key'],"|",issue['outwardIssue']['fields']['summary'] )
            fstr = "MTV|" + issue['id'] + "|" + issue['outwardIssue']['key'] + "|" + issue['outwardIssue']['fields']['summary'] + "|" + issue['outwardIssue']['fields']['issuetype']['name'] + "|" + issue['outwardIssue']['fields']['status']['name'] + "\n"
            f.write(fstr)
            mtv = jira.issue(issue['outwardIssue']['key'])
            featureList = mtv.raw['fields']['issuelinks']
            for feature in featureList:
                try:
                    fstr = "    Feature|" + feature['id'] + "|" + feature['outwardIssue']['key'] + "|" + feature['outwardIssue']['fields']['summary'] + "|" + feature['outwardIssue']['fields']['issuetype']['name'] + "|" + feature['outwardIssue']['fields']['status']['name'] + "\n"
                    f.write(fstr)                    
                    jql = 'issuetype = "User Story" and "Parent Feature Key" ~ "' + feature['outwardIssue']['key'] + "\""
                    usList = jira.search_issues(jql_str= jql)                    
                    for us in usList:
                        try:
                            if str(us.fields.status) not in ['Accepted','Cancelled']:
                                fstr = "        US|" + us.key +"|"+ str(us.fields.status) + "\n"
                                f.write(fstr)
                        except KeyError:
                            continue 
                except KeyError:
                    continue
        except KeyError:
            continue        

def main(argv):    
    validate()

if __name__ == "__main__":
    main(sys.argv[1:])

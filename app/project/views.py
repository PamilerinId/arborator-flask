from flask import render_template
from flask_login import login_required
from app import requires_access_level
from . import home



def list_projects():
    """
    List all projects
    """
    check_admin()

    projects = Project.query.all()

    return render_template('project/projects.html',
                           projects=projects, title="Projects")

@project.route('/<project_name>')
def projectpage(project_name):
    """
    Individual project pages
    """    
    ##check if user assigned
    ##read in user congig files
    ##associate user with particular project

    return render_template('project/project.html',project_name=project_name, title=project_name)




######################ignore for now####################################################################
###################33db operations###############################33
def export(textname, exportNumber, exportType, project):
    	#textname=textname.encode("utf-8")
	print "<h2>Exporting",textname.encode("utf-8"),"(text number",exportNumber,")</h2>"
	
	if textname:
		fc,users,sc,doublegovs=sql.exportAnnotations(int(exportNumber), textname, exportType )
		if fc==0: 	print "<div style='padding:10;' class='ui-state-error ui-corner-all'>No files were exported, probably because the file is assigned to nobody.</div><br/>"
		else:		
			print "Exported",fc,"files and a total of",sc,"sentences.<br/><br/>"
			if exportType in ["allconll","allxml"]:
				print "Exported all existing annotated trees into",
				if exportType =="allconll": print textname.encode("utf-8")+".user.trees.conll files.<br/>"
				else: print textname.encode("utf-8")+".user.trees.rhaps.xml files.<br/>"
			else: 
				print "Exported complete files for each assignment into"
				if exportType =="todoconll": print textname.encode("utf-8")+".user.complete.conll10 files.<br/>"
				else: print textname.encode("utf-8")+".user.complete.rhaps.xml files.<br/>"
		print "<br/><div style='padding:10;'  class='ui-state-highlight ui-corner-all'>",
		if fc==1:print "The export file for",users[0],"is"
		else: print "All the",fc,"export files (for",(", ".join(users)).encode("utf-8")+") are"
		print " in the export folder <strong style='color:#DD137B'><a href='projects/{project}/export' target='_blank'>inside the project folder</a></strong> on the server.</div><br/>".format(project=project.replace("'","\\'").replace('"','\\"').encode("utf-8"))
		if doublegovs: print "<div style='padding:10;' class='ui-state-error ui-corner-all'>Achtung!<br/> The annotation contains multiple governors for one or more nodes. The lines have been doubled, and thus this is not a common Conll format!</div>"
	else:
		print "problem: no textname"


def reaction(project,projectconfig,sql,userid,form,query):
    	"""
	contains reaction to actions, eg. uploading, erasing, exporting, ...
	"""
	filename = form.getvalue("filename",None)
	if filename: # upload file	
		from lib.treebankfiles import uploadConll
		filetype = form.getvalue("filetype",None)
		print "trying to upload",filename,filetype,"into the database of the project",project.encode("utf-8")
		if filetype in ["conll4","conll10","conll14"]:
			print "---------- here we go"
			nrsentences = uploadConll(sql,filename)
			print """<div class="ui-widget ui-widget-content ui-corner-all box">I added {nrsentences} sentences from {filename}.</div>""".format(nrsentences=nrsentences,filename=filename)
		else:	print """<div class="ui-widget ui-widget-content ui-corner-all box">Strange filetype: {filename}.</div>""".format(filename=filename)

	eraseNumber = form.getvalue("eraseNumber",None)
	if eraseNumber: # erase text
		print "erasing text number ",eraseNumber,"<br/>"
		sc=sql.removeText(int(eraseNumber))
		print "erased",sc,"sentences."

	#statustextid = form.getvalue("statustextid",None)
	#if statustextid: # erase text
		##print "statustextid, text number:",statustextid,"<br/>"
		#sql.statustext(int(statustextid),userid)

	exportNumber = form.getvalue("exportNumber",None)
	textname=None
	if exportNumber: # export text
		print '<div class="ui-widget ui-widget-content ui-corner-all box" >'
		
		textname = form.getvalue("textname",None)
		exportType = form.getvalue("exportType",None)
		#print exportNumber,type(exportNumber)
		exportNumber=int(exportNumber)
		if exportNumber==-1 :
			for t,tid in sorted( [(t,tid) for tid,t,nrtokens in sql.getall(None, "texts", None, None)]):
				export(t, tid, exportType, project)
			
		else: export(textname, exportNumber, exportType, project)
		
		print '</div>'

		
	userchoice = form.getlist('userchoice')
	textid = form.getvalue("textid",None)

	if userchoice and textid: # change todos
		removeid = int(form.getvalue("removeid",0))
		validator = int(form.getvalue("validator",0))
		if removeid:
			sql.removetextfromuser(int(textid),removeid)
		else:
			u=userchoice[0].split("(")[-1][:-1]
			sql.addtext2user(textid,u,validator)
			
	
	exochoice = form.getvalue("exochoice",None)
	if exochoice:
		
		textid = form.getvalue("textid",None)
		exotoknum = form.getvalue("exotoknum",None)
		
		print "changing exostatus of text id",textid,"to",exochoice
		sql.setExo(textid, exochoice, exotoknum)
		
	
	if query: # search results	
		print """<div class="ui-widget ui-widget-content ui-corner-all box"  style="text-align:-moz-center;">"""
		
		res = sql.snippetSearch(query)
		if res: 
			print "<h2>Search results for {query}:</h2>".format(query=query)
			print res.encode("utf-8")
		else: print "no results for {query}</h2>".format(query=query)
		print """</div>"""




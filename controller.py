#!/usr/bin/python3
# Creative Commons Legal Code
# 
# CC0 1.0 Universal
# 
#     CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
#     LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
#     ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
#     INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
#     REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
#     PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
#     THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
#     HEREUNDER.
# 
# Statement of Purpose
# 
# The laws of most jurisdictions throughout the world automatically confer
# exclusive Copyright and Related Rights (defined below) upon the creator
# and subsequent owner(s) (each and all, an "owner") of an original work of
# authorship and/or a database (each, a "Work").
# 
# Certain owners wish to permanently relinquish those rights to a Work for
# the purpose of contributing to a commons of creative, cultural and
# scientific works ("Commons") that the public can reliably and without fear
# of later claims of infringement build upon, modify, incorporate in other
# works, reuse and redistribute as freely as possible in any form whatsoever
# and for any purposes, including without limitation commercial purposes.
# These owners may contribute to the Commons to promote the ideal of a free
# culture and the further production of creative, cultural and scientific
# works, or to gain reputation or greater distribution for their Work in
# part through the use and efforts of others.
# 
# For these and/or other purposes and motivations, and without any
# expectation of additional consideration or compensation, the person
# associating CC0 with a Work (the "Affirmer"), to the extent that he or she
# is an owner of Copyright and Related Rights in the Work, voluntarily
# elects to apply CC0 to the Work and publicly distribute the Work under its
# terms, with knowledge of his or her Copyright and Related Rights in the
# Work and the meaning and intended legal effect of CC0 on those rights.
# 
# 1. Copyright and Related Rights. A Work made available under CC0 may be
# protected by copyright and related or neighboring rights ("Copyright and
# Related Rights"). Copyright and Related Rights include, but are not
# limited to, the following:
# 
#   i. the right to reproduce, adapt, distribute, perform, display,
#      communicate, and translate a Work;
#  ii. moral rights retained by the original author(s) and/or performer(s);
# iii. publicity and privacy rights pertaining to a person's image or
#      likeness depicted in a Work;
#  iv. rights protecting against unfair competition in regards to a Work,
#      subject to the limitations in paragraph 4(a), below;
#   v. rights protecting the extraction, dissemination, use and reuse of data
#      in a Work;
#  vi. database rights (such as those arising under Directive 96/9/EC of the
#      European Parliament and of the Council of 11 March 1996 on the legal
#      protection of databases, and under any national implementation
#      thereof, including any amended or successor version of such
#      directive); and
# vii. other similar, equivalent or corresponding rights throughout the
#      world based on applicable law or treaty, and any national
#      implementations thereof.
# 
# 2. Waiver. To the greatest extent permitted by, but not in contravention
# of, applicable law, Affirmer hereby overtly, fully, permanently,
# irrevocably and unconditionally waives, abandons, and surrenders all of
# Affirmer's Copyright and Related Rights and associated claims and causes
# of action, whether now known or unknown (including existing as well as
# future claims and causes of action), in the Work (i) in all territories
# worldwide, (ii) for the maximum duration provided by applicable law or
# treaty (including future time extensions), (iii) in any current or future
# medium and for any number of copies, and (iv) for any purpose whatsoever,
# including without limitation commercial, advertising or promotional
# purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
# member of the public at large and to the detriment of Affirmer's heirs and
# successors, fully intending that such Waiver shall not be subject to
# revocation, rescission, cancellation, termination, or any other legal or
# equitable action to disrupt the quiet enjoyment of the Work by the public
# as contemplated by Affirmer's express Statement of Purpose.
# 
# 3. Public License Fallback. Should any part of the Waiver for any reason
# be judged legally invalid or ineffective under applicable law, then the
# Waiver shall be preserved to the maximum extent permitted taking into
# account Affirmer's express Statement of Purpose. In addition, to the
# extent the Waiver is so judged Affirmer hereby grants to each affected
# person a royalty-free, non transferable, non sublicensable, non exclusive,
# irrevocable and unconditional license to exercise Affirmer's Copyright and
# Related Rights in the Work (i) in all territories worldwide, (ii) for the
# maximum duration provided by applicable law or treaty (including future
# time extensions), (iii) in any current or future medium and for any number
# of copies, and (iv) for any purpose whatsoever, including without
# limitation commercial, advertising or promotional purposes (the
# "License"). The License shall be deemed effective as of the date CC0 was
# applied by Affirmer to the Work. Should any part of the License for any
# reason be judged legally invalid or ineffective under applicable law, such
# partial invalidity or ineffectiveness shall not invalidate the remainder
# of the License, and in such case Affirmer hereby affirms that he or she
# will not (i) exercise any of his or her remaining Copyright and Related
# Rights in the Work or (ii) assert any associated claims and causes of
# action with respect to the Work, in either case contrary to Affirmer's
# express Statement of Purpose.
# 
# 4. Limitations and Disclaimers.
# 
#  a. No trademark or patent rights held by Affirmer are waived, abandoned,
#     surrendered, licensed or otherwise affected by this document.
#  b. Affirmer offers the Work as-is and makes no representations or
#     warranties of any kind concerning the Work, express, implied,
#     statutory or otherwise, including without limitation warranties of
#     title, merchantability, fitness for a particular purpose, non
#     infringement, or the absence of latent or other defects, accuracy, or
#     the present or absence of errors, whether or not discoverable, all to
#     the greatest extent permissible under applicable law.
#  c. Affirmer disclaims responsibility for clearing rights of other persons
#     that may apply to the Work or any use thereof, including without
#     limitation any person's Copyright and Related Rights in the Work.
#     Further, Affirmer disclaims responsibility for obtaining any necessary
#     consents, permissions or other rights required for any use of the
#     Work.
#  d. Affirmer understands and acknowledges that Creative Commons is not a
#     party to this document and has no duty or obligation with respect to
#     this CC0 or use of the Work.

import sys
import re
import hashlib
import requests
import docker
import json
import time
from xml.etree import ElementTree

import psycopg2

with open("config.json") as json_config_file:
	config = json.load(json_config_file)

POSTGRESHOST = "localhost"
POSTGRESPORT = 5433
if "postgresql" in config:
	if "db" in config["postgresql"] and "user" in config["postgresql"] and "password" in config["postgresql"]:
		POSTGRESDB = config["postgresql"]["db"]
		POSTGRESUSER = config["postgresql"]["user"]
		POSTGRESPASS = config["postgresql"]["password"]
	else:
		print('Missing postgresql config')
		sys.exit(1)
	if "port" in config["postgresql"]:
		POSTGRESPORT = config["postgresql"]["port"]
	if "host" in config["postgresql"]:
		POSTGRESHOST = config["postgresql"]["host"]

conn_auth = psycopg2.connect("dbname=" + POSTGRESDB + " user=" + POSTGRESUSER + " password=" + POSTGRESPASS + " host=" + POSTGRESHOST + " port=" + POSTGRESPORT)

DAEMON = False
BBB_URL = ""
BBB_SECRET = ""
BBB_RTMP_PATH = ""
BBB_WEB_STREAM = ""
BBB_RES = "1920x1080"

if "daemon" in config:
	DAEMON = config["daemon"]
if "bbb_url" in config:
	BBB_URL = config["bbb_url"]
if "bbb_secret" in config:
	BBB_SECRET = config["bbb_secret"]
if "rtmp_path" in config:
	BBB_RTMP_PATH = config["rtmp_path"]
if "web_stream" in config:
	BBB_WEB_STREAM = config["web_stream"]
if "bbb_res" in config:
	BBB_RES = config['bbb_res']

client = docker.from_env()

def get_running_rooms():
	
	URL = BBB_URL
	secret = BBB_SECRET
	
	APIURL=URL + 'api/'
	
	apimethod='getMeetings'
	querystring=''
	
	h = hashlib.sha1((apimethod+querystring+secret).encode('utf-8'))
	checksum = h.hexdigest()
	
	if len(querystring) > 0:
		querystring = querystring + '&'
	
	requesturl = APIURL + apimethod + '?' + querystring + 'checksum=' + checksum
	
	response = requests.get(requesturl)
	tree = ElementTree.fromstring(response.content)
	
	if tree.find('returncode').text != 'SUCCESS':
		print('error getting API data')
		sys.exit(1)
	meetings = tree.find('meetings')
	
	mids = {}
	if meetings:
		for m in meetings.iter('meeting'):
			user_no = m.find('participantCount').text
			users = []
			for u in m.find('attendees').iter('attendee'):
				users.append(u.find('fullName').text)
			meetid = m.find('meetingID').text
			meetid_int = m.find('internalMeetingID').text
			mids[meetid] = {'bbb_meet_id': meetid_int, 'users': users, 'user_no': int(user_no) }
	return mids

def check_streaming_rooms(meetingids):
	streaming_rooms = {}
	cur = conn_auth.cursor()
	
	for bbbid in meetingids.keys():
		cur.execute("SELECT uid,attendee_pw,room_settings FROM rooms WHERE bbb_id = %s;", (bbbid,))
		res = cur.fetchall()
		if res:
			roompath = res[0][0]
			attendeepw = res[0][1]
			roomdata = json.loads(res[0][2])
			if 'streaming' in roomdata:
				if roomdata['streaming'] == True:
					meetingids[bbbid]['roompath'] = roompath
					meetingids[bbbid]['attendeepw'] = attendeepw
					meetingids[bbbid]['roomdata'] = dict(roomdata)
					streaming_rooms[bbbid] = meetingids[bbbid]
	return streaming_rooms

def check_container_running(bbbid):
	try:
		container = client.containers.get('strm_'+bbbid)
	except docker.errors.NotFound:
		return False
	return True

def start_streaming(meetingids):
	streamCount=0
	client.containers.prune()
	for bbbid in meetingids.keys():
		dockerenv = {
			'BBB_URL': BBB_URL,
			'TZ': 'Europe/Vienna',
			'BBB_RESOLUTION': BBB_RES,
			'BBB_START_MEETING': 'false',
			'BBB_MEETING_ID': bbbid,
			'FFMPEG_STREAM_THREADS': '0',
			'BBB_STREAM_URL': BBB_RTMP_PATH + meetingids[bbbid]['roompath'],
			'FFMPEG_STREAM_VIDEO_BITRATE': '4000',
			'BBB_SECRET': BBB_SECRET,
			'BBB_SHOW_CHAT': 'false',
			'BBB_USER_NAME': 'Streaming User',
			'BBB_CHAT_STREAM_URL': BBB_WEB_STREAM+meetingids[bbbid]['roompath']+'/',
			'BBB_ATTENDEE_PASSWORD': meetingids[bbbid]['attendeepw']
		}
		
		if not check_container_running(bbbid) and meetingids[bbbid]['user_no'] > 0 and not 'Streaming User' in meetingids[bbbid]['users']:
			container = client.containers.run('aauzid/bigbluebutton-livestreaming', name='strm_'+bbbid, shm_size='2gb', environment=dockerenv, detach=True)
			streamCount += 1
			print('Started container strm_'+bbbid+'\n')
	return streamCount
def terminate_orphaned(meetingids):
	containers = client.containers.list()
	for container in containers:
		if '/strm_' == container.attrs['Name'][:6]:
			name = container.attrs['Name'][6:]
			
			if not name in meetingids:
				container.kill()
			else:
				if meetingids[name]['user_no'] == 1 and 'Streaming User' in meetingids[name]['users']:
					container.kill()
					print('Stopping container /strm_' == container.attrs['Name'][:6])
	client.containers.prune()
		
while True:
	delayTimout = 10
	mids = get_running_rooms()
	stream_mids  = check_streaming_rooms(mids)
	retVal=start_streaming(stream_mids)
	if retVal > 0:
		# Delay next loop a little to allow container to start
		delayTimout = 30
	terminate_orphaned(stream_mids)
	if DAEMON:
		time.sleep(delayTimout)
	else:
	    break

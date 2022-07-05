import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 이메일 로그인 계정 입력
sender = ''
email = ""
password = ""
# 수신자 이메일 입력
receiver = "hipex@googlegroups.com"

def smtp_setting(type, email, password):
    mail_type = None
    port = 587
    if type == 'naver':
        mail_type = 'smtp.naver.com'
    elif type == 'gmail':
        mail_type = 'smtp.gmail.com'
    else:
        mail_type = 'smtp.gmail.com'

    # SMTP 세션 생성
    smtp = smtplib.SMTP(mail_type, port)
    smtp.set_debuglevel(True)

    # SMTP 계정 인증 설정
    smtp.ehlo()
    smtp.starttls() # TLS 사용시 호출
    smtp.login(email, password) # 로그인

    return smtp

def send_multipart_mail(sender, receiver, email, password, subject, content):
    # SMTP 세션 생성
    smtp = smtp_setting('gmail', email, password)
    try:
        # 이메일 데이터 설정
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender  # 송신자
        msg['To'] = receiver  # 수신자
        # msg['To'] = ",".join(receiver)    # 여러명의 수신자일 경우

        # 일반 텍스트 형식의 문자열
        part1 = MIMEText(content['plain'], 'plain')
        # HTML 형식의 문자열
        part2 = MIMEText(content['html'], 'html')

        msg.attach(part1)
        msg.attach(part2)

        # 메일 전송
        smtp.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        print('error', e)
    finally:
        if smtp is not None:
            smtp.quit()

import argparse
parser = argparse.ArgumentParser(description = '프로그램 설명')
parser.add_argument('meetingLink', help = 'Notion 미팅 페이지 링크를 입력하라')
parser.add_argument('--meetingday', help = '미팅 요일 소문자로 day까지 정확하게 쳐야 함. 초기값은 금요일.')
parser.add_argument('--meetinghour', default='1600', help = '미팅 시간 HHmm꼴로 나타내면 됨. 초기값은 1600.')
args = parser.parse_args()

meetinglink = args.meetingLink
import datetime
day = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()-4)
dayname = '금'
if args.meetingday == 'thursday':
    day = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()-3)
    dayname = '목'
elif args.meetingday == 'wednesday':
    day = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()-2)
    dayname = '수'
elif args.meetingday == 'tuesday':
    day = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()-8)
    dayname = '화'
elif args.meetingday == 'monday':
    day = datetime.date.today() - datetime.timedelta(days=datetime.date. today().weekday()-7)
    dayname = '월'

hour = int(args.meetinghour[0:2])
minute = int(args.meetinghour[2:4])
meetingtime = datetime.datetime.combine(day, datetime.time(hour,minute,00))
meetingtime_CEST = meetingtime.astimezone(datetime.timezone(datetime.timedelta(hours=2)))
meetingtime_CET = meetingtime.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
if 3 < int((datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()-6)).strftime("%m")) <11:
    CERN_time = meetingtime_CEST.strftime("%H:%M")
    CERN_time_name = "CEST"
else:
    CERN_time = meetingtime_CET.strftime("%H:%M")
    CERN_time_name = "CET"
meetingdate_KOR = meetingtime.strftime("%Y년 %m월 %d일")
meetingdate_ENG = meetingtime.strftime("%d %b. %Y")
meetingtime_KST = meetingtime.strftime("%H:%M")

send_multipart_mail(sender, receiver, email, password, '[미팅공지] ' + str(day.strftime("%Y.%m.%d")) + ' HIPEx Local Meeting',
    {'plain' : '[미팅공지] ' + str(day.strftime("%Y.%m.%d")) + ' HIPEx Local Meeting',
    'html' : f"""
    <html>
        <head></head>
        <body>
            <p>
            안녕하십니까?<br>
            이번 주 HIPEx Local Meeting 공지 메일을 보내드립니다.<br><br>
            <b>{meetingdate_KOR}({dayname}) {meetingtime_KST} KST:UTC+9 ({CERN_time} {CERN_time_name}:UTC+2)</b>에  <b>부산대학교 공동연구기기동 210호 (Offline)</b> 에서 진행될 예정입니다.<br>
            <b>CERN</b> 사이드에서는 KST 기준 {meetingtime_KST}, <b>{CERN_time_name} 기준 {CERN_time}</b>에 접속하면 됩니다.<br><br>
            Meeting 페이지는 Notion 계정으로 접속가능합니다. Notion 가입을 하지 않은 분은 이전에 초대 이메일을 받은 이메일 주소로 가입한 후 접속해주시길 부탁드립니다.<br>
            접속이 불가할 경우, 권민재에게 연락주시면 후속 처리가 가능하니, 연락바랍니다.<br><br>
            <a href="{meetinglink}">미팅페이지</a><br>
            <a href="https://pusan.zoom.us/j/838738055">Zoom 링크</a> <b>(Zoom@PNU. MeetingID: <span style="color: #0000ff;"><U>838-738-055</U></span> Password: <span style="color: #5800FD;"><U>hipex</U></span>)</b><br><br>      
            미팅에 발표 예정인 자료는 미팅 시작 시간 이전에 해당 미팅 페이지에 업로드 바랍니다.<br>
            ※ 미팅 지각 기준: 미팅 프로토콜 작성 담당자 컴퓨터 시간 기준<br>
            ※ 미팅 지각 시 1분당 500원 벌금. 무단 결석 시 미팅이 진행된 시간만큼 벌금<br>
            ※ 미팅 지각 시 <a href="https://www.notion.so/cb737bee78894091a67faa682ede6b82">지각비 테이블</a> 에 기록됩니다. 확인해 주시고 정산해주시면 됩니다.<br><br><br>
            감사합니다.<br>
            최용준 드림<br><br><br>
            ————————————————————————————————<br><br>
            Dear all,<br>
            I am sending an announcement mail about the HIPEx Local Meeting of this week.<br><br>
            It will be held on <b> 206ho - 311dong in Pusan University</b> at <b>{meetingtime_KST} KST:UTC+9 ({CERN_time} {CERN_time_name}:UTC+2) {meetingdate_ENG}</b>.<br>
            Person on <b>CERN side</b> should contact us at {meetingtime_KST} KST or <b>{CERN_time} {CERN_time_name}</b><br><br>
            You can access the meeting page with your notion account. If you didn't sign up to the notion, then you can enter that after signing up with an e-mail address which has invitation mail.<br>
            If you cannot access it, contact Minjae Kwon. He will solve your problem.<br><br>
            <a href="{meetinglink}">Meeting page</a><br>
            <a href="https://pusan.zoom.us/j/838738055">Zoom link</a> <b>(Zoom@PNU. MeetingID: <span style="color: #0000ff;"><U>838-738-055</U></span> Password: <span style="color: #0000ff;"><U>hipex</U></span></b>)<br><br>
            Meeting material should be uploaded at the corresponding meeting page before the start of the meeting.<br>
            ※ Point of lateness: Computer time of meeting protocol secretary<br>
            ※ A lateness fine rate is ₩500/1min. When absent without permission, the lateness fine is the same as a run-time of meeting times the lateness fine rate.<br>
            ※ The lateness is recorded at <a href="https://www.notion.so/cb737bee78894091a67faa682ede6b82">lateness fine table</a>. Check and pay please.<br><br><br>
            Best regards,<br>
            Yongjun Choi<br><br><br>
            ————————————————————————————————<br><br>
            Yongjun Choi (최용준)<br><br>
            Building #311 - 206, HIPEx (Heavy Ion Physics Experiment Lab), Pusan National University, Republic of Korea<br>
            Department of Physics, Pusan National University, Republic of Korea<br><br><br><br>
            +82 10 8229 2909 (Mobile.)
            </p>
        </body>
    </html>
    """})
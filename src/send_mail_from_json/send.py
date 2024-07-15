import os
os.chdir(os.path.dirname(__file__))
# 更换工作目录

import logging
import datetime

logging.basicConfig(
                    filename=f"../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SMFJ>Send")
# 配置日志信息

import smtplib
import json
from email.mime.text import MIMEText
from email.header import Header

class Send:
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        with open(self.json_file, "r", encoding="utf-8") as f:
            self.data = eval(repr(json.load(f))) # type: dict
        self._from = {
            "email": self.data["from"],
            "pwd": self.data["password"],
            "name": self.data["name"]
        }
        if (self.data["encryption"] == "ssl"):
            self.smtp_obj = smtplib.SMTP_SSL(self.data["smtp_server"], self.data["smtp_port"], timeout=self.data["timeout"])
        elif (self.data["encryption"] == "tls")or(self.data["encryption"] == "starttls"):
            self.smtp_obj = smtplib.SMTP(self.data["smtp_server"], self.data["smtp_port"], timeout=self.data["timeout"])
            self.smtp_obj.starttls()
        elif (self.data["encryption"] == None):
            self.smtp_obj = smtplib.SMTP(self.data["smtp_server"], self.data["smtp_port"], timeout=self.data["timeout"])
        else:
            raise Exception("Encryption type not supported")
        self.recipients = self.data["emails"]
        self.smtp_obj.login(self._from["email"], self._from["pwd"])
        for recipient in self.recipients:
            self.message = MIMEText(recipient["body"], "plain", "utf-8")
            self.message["From"] = Header(self._from["name"], "utf-8")
            self.message["To"] = recipient["to"]
            self.message["Subject"] = Header(recipient["subject"], "utf-8")
            self.smtp_obj.sendmail(from_addr=self._from["email"], to_addrs=recipient["to"], msg=self.message.as_string())
            logger.info(f"Send complete to {repr(recipient)}")
        self.smtp_obj.quit()
        

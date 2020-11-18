#!/bin/bash
#CR_AUDIT=/usr/local/linkbynet/scripts/Audit_Reseau/CR

#/usr/bin/mutt -e "set content_type=text/html" a.dumur@linkbynet.com -s "[AUDIT] Audit Du `/bin/date +%d-%m-%Y`" -i $CR_AUDIT  </dev/null
#/usr/bin/mutt -e "set content_type=text/html" admin-rsx@linkbynet.com -s "[AUDIT] Audit Du `/bin/date +%d-%m-%Y`" -i $CR_AUDIT  </dev/null


/usr/bin/mutt -e "set content_type=text/html" admin-rsx@linkbynet.com -s "[AUDIT] Audit Du `/bin/date +%d-%m-%Y`" -a /usr/local/linkbynet/scripts/Audit_Reseau/AuditReport.xlsx < /usr/local/linkbynet/scripts/Audit_Reseau/CR



#/usr/bin/mutt -e "set content_type=text/html" admin-rsx@linkbynet.com -s "[AUDIT] Audit Du `/bin/date +%d-%m-%Y`" -a AuditReport.xlsx < CR


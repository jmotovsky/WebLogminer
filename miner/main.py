from typing import Dict, List
import packages.weblogmining as wlm

base_data_dir = "./data/"
input_file = base_data_dir + 'week.log'
output_file = base_data_dir + 'cleanData.log'
stt_q = 151

entry_role: Dict[str, List[str]] = {
    'IN/STUDENT': [
        '10.160.0.***',
        '10.160.1.***',
        '10.160.2.0**',
        '10.160.2.1**',
        '10.160.3.***',
    ],
    'IN/ZAMEST': [
        '10.160.2.2**',
        '10.160.***.***',
    ],
}
default_entry_role: str = 'OUT'

wlm.clean_up_data(input_file, output_file)
wlm.init_sqlite(base_data_dir)
wlm.session_identifier(output_file, stt_q)
wlm.postprocessing_data(entry_role, default_entry_role)

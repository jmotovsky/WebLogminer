from timeit import default_timer as timer
from packages.weblogmining.datatransformation.process import process_base_data, process_pre_robots, process_robots

base_data_dir = "../../../projects/WebLogMining/data/"
input_file_name = base_data_dir + 'week.log'
temp_file_name = base_data_dir + 'temp.log'
final_file_name = base_data_dir + 'cleanData.log'

start = timer()

pre_robots_clean_data = {}
temp_file = open(temp_file_name, 'w')
with open(input_file_name) as f:
    for line in f:
        out = process_base_data(line)
        if out:
            transform_data = '\t'.join(out.values()) + '\n'
            temp_file.write(transform_data)
            out_robots = process_pre_robots(transform_data)
            if out_robots and out_robots['IP'] not in pre_robots_clean_data:
                out_ip = out_robots['IP']
                pre_robots_clean_data[out_ip] = out_robots

temp_file.close()

final_file = open(final_file_name, 'w')
with open(temp_file_name) as f:
    for line in f:
        append = True
        for key, value in pre_robots_clean_data.items():
            out = process_robots(line, value['IP'], value['Agent'])
            if out:
                append = False
                break

        if append:
            final_file.write(line)

final_file.close()
end = timer()
print(end - start)

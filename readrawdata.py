import countfunc as count
OS = 'UB20'  # os
HH = 23  # hour
MM = 8  # minute
S1 = 4  # second on experiment start
S2 = 10  # second on migration start
S3 = 18  # second on migration end
S4 = 21  # second on experiment end
str_HH = str(HH) if HH >= 10 else '0'+str(HH)
str_MM = str(MM) if MM >= 10 else '0'+str(MM)
str_S1 = str(S1) if S1 >= 10 else '0'+str(S1)
str_S2 = str(S2) if S2 >= 10 else '0'+str(S2)
str_S3 = str(S3) if S3 >= 10 else '0'+str(S3)
time_title = str_HH + "-" + str_MM + "-" + str_S1 + "-" + str_S2 + "-" + str_S3
f = open("raw/"+OS+"_" + time_title + "_disk", "r", encoding='utf-8')
disks = f.readlines()
f.close()
f = open("raw/"+OS+"_" + time_title + "_mem", "r", encoding='utf-8')
mems = f.readlines()
f.close()
f = open("raw/"+OS+"_" + time_title + "_itr", "r", encoding='utf-8')
itrs = f.readlines()
f.close()
result = []
# jump to time point, before migration
time_point_0 = str_HH + ":" + str_MM + ":" + str_S1
_, itr_0 = count.itr_count_at_time(time_point_0, itrs)
_, disk_0 = count.disk_speed_at_time(time_point_0, disks)
_, mem_0 = count.mem_speed_at_time(time_point_0, mems)
last = [time_point_0, disk_0, mem_0, itr_0[0], itr_0[1], itr_0[2], itr_0[3]]
#result.append([time_point_0, 1.0, 1.0, 0, 0, 0, 0, 0])
mean_disk = [last[1]]
mean_mem = [last[2]]
for s in range(S1 + 1, S2):
    str_s = str(s) if s >= 10 else '0'+str(s)
    time_point = str_HH + ":" + str_MM + ":" + str_s
    tmp = ['', 0.0, 0.0, 0, 0, 0, 0]
    tmp[0] = time_point
    dflag, tmp[1] = count.disk_speed_at_time(time_point, disks)
    tmp[1] = tmp[1] if dflag else last[1]
    mean_disk.append(tmp[1])
    mflag, tmp[2] = count.mem_speed_at_time(time_point, mems)
    tmp[2] = tmp[2] if mflag else last[2]
    mean_mem.append(tmp[2])
    flag, itr = count.itr_count_at_time(time_point, itrs)
    tmp[3] = itr[0] if flag else last[3]
    tmp[4] = itr[1] if flag else last[4]
    tmp[5] = itr[2] if flag else last[5]
    tmp[6] = itr[3] if flag else last[6]
    result.append([time_point, (tmp[1] - last[1]) / last[1], (tmp[2] - last[2]) / last[2],
                   tmp[3] - last[3], tmp[4] - last[4], tmp[5] - last[5], tmp[6] - last[6], 0])
    last = tmp
mean_disk_value = sum(mean_disk) / len(mean_disk)
mean_mem_value = sum(mean_mem) / len(mean_mem)
# speed normalization
for i in range(len(result)):
    result[i][1] = (mean_disk[i] - mean_disk_value) / mean_disk_value
    result[i][2] = (mean_mem[i] - mean_mem_value) / mean_mem_value
# during migration
for s in range(S2, S3 + 1):
    str_s = str(s) if s >= 10 else '0' + str(s)
    time_point = str_HH + ":" + str_MM + ":" + str_s
    tmp = ['', 0.0, 0.0, 0, 0, 0, 0]
    tmp[0] = time_point
    dflag, tmp[1] = count.disk_speed_at_time(time_point, disks)
    tmp[1] = tmp[1] if dflag else last[1]
    mflag, tmp[2] = count.mem_speed_at_time(time_point, mems)
    tmp[2] = tmp[2] if mflag else last[2]
    flag, itr = count.itr_count_at_time(time_point, itrs)
    tmp[3] = itr[0] if flag else last[3]
    tmp[4] = itr[1] if flag else last[4]
    tmp[5] = itr[2] if flag else last[5]
    tmp[6] = itr[3] if flag else last[6]
    result.append([time_point, (tmp[1] - mean_disk_value) / mean_disk_value, (tmp[2] - mean_mem_value) / mean_mem_value,
                   tmp[3] - last[3], tmp[4] - last[4], tmp[5] - last[5], tmp[6] - last[6], 1])
    last = tmp
# after migration
for s in range(S3 + 1, S4):
    str_s = str(s) if s >= 10 else '0' + str(s)
    time_point = str_HH + ":" + str_MM + ":" + str_s
    tmp = ['', 0.0, 0.0, 0, 0, 0, 0]
    tmp[0] = time_point
    dflag, tmp[1] = count.disk_speed_at_time(time_point, disks)
    tmp[1] = tmp[1] if dflag else last[1]
    mflag, tmp[2] = count.mem_speed_at_time(time_point, mems)
    tmp[2] = tmp[2] if mflag else last[2]
    flag, itr = count.itr_count_at_time(time_point, itrs)
    tmp[3] = itr[0] if flag else last[3]
    tmp[4] = itr[1] if flag else last[4]
    tmp[5] = itr[2] if flag else last[5]
    tmp[6] = itr[3] if flag else last[6]
    result.append([time_point, (tmp[1] - mean_disk_value) / mean_disk_value, (tmp[2] - mean_mem_value) / mean_mem_value,
                   tmp[3] - last[3], tmp[4] - last[4], tmp[5] - last[5], tmp[6] - last[6], 0])
    last = tmp
# output
f = open("dataset", "a", encoding='utf-8')
for r in result:
    for rr in r:
        f.write(str(rr)+' ')
    f.write('\n')
f.close()
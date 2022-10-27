##compute mem speed per second
def mem_speed_at_time(time_point, mems):
    count = 0
    flag = False
    tp_mem = []
    for l in mems:
        if flag:
            if count > 0:
                count -= 1
                continue
            else:
                flag = False
                r = l.split(",")
                r1 = float(r[2].split(' ')[1])
                r2 = float(r[3].split(' ')[1])
                if str('GB/s') == r[3].split(' ')[2].strip():
                    r2 *= 1024
                tp_mem.append([r1, r2])
        if not flag and l.find(time_point) != -1:
            count = 2
            flag = True
    tt = 0.0
    for t in tp_mem:
        tt += t[0]
    result = 0.0
    for t in tp_mem:
        result += t[0] / tt * t[1]
    return len(tp_mem) > 0, result


##compute disk speed per second
def disk_speed_at_time(time_point, disks):
    count = 0
    flag = False
    tp_disk = []
    for l in disks:
        if flag:
            if count > 0:
                count -= 1
                continue
            else:
                flag = False
                r = l.split(",")
                r1 = float(r[2].split(' ')[1])
                r2 = float(r[3].split(' ')[1])
                if str('GB/s') == r[3].split(' ')[2].strip():
                    r2 *= 1024
                tp_disk.append([r1, r2])
        if not flag and l.find(time_point) != -1:
            count = 2
            flag = True
    tt = 0.0
    for t in tp_disk:
        tt += t[0]
    result = 0.0
    for t in tp_disk:
        result += t[0] / tt * t[1]
    return len(tp_disk) > 0, result


##get itr number per second
def itr_count_at_time(time_point, itrs):
    flag = False
    tp_itr = []
    itr = []
    for l in itrs:
        if flag:
            i = l.split(' ')
            i = [x.strip() for x in i if x.strip() != '']
            if str('0:') == i[0]:
                itr.append(int(i[1]))
                continue
            if str('25:') == i[0]:
                itr.append(int(i[1]))
                continue
            if str('27:') == i[0]:
                itr.append(int(i[1]))
                continue
            if str('29:') == i[0]:
                itr.append(int(i[1]))
                flag = False
                tp_itr.append(itr)
                itr = []
                continue
        if not flag and l.find(time_point) != -1:
            flag = True
    # start = tp_itr[0]
    # end = tp_itr[-1]
    # result = [end[0]-start[0], end[1]-start[1], end[2]-start[2], end[3]-start[3]]
    if len(tp_itr) > 0:
        result = tp_itr[-1]
    else:
        result = []
    return len(result) > 0, result

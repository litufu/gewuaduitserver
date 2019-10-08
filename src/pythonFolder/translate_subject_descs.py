from constant import subject_descs

def handle_desc(direction_descs,item,only,direction):

    if isinstance(direction_descs, dict):
        # 根据关键字判断后再根据对方科目判断，仅限一个关键词组
        keywords = direction_descs["keywords"]
        contain_descs = direction_descs["contain_event"]
        not_contain_descs = direction_descs["not_contain_event"]
        if isinstance(contain_descs, str):
            event = contain_descs
            if only:
                item["judge"].append({
                    "logic": "and",
                    "condition": [
                        {"subject_direction": direction},
                        {"same_subjects_only_one":True},
                        {"entry_keywords":keywords}
                     ],
                    "event": event,
                   })
            else:
                item["judge"].append({
                    "logic": "and",
                    "condition": [
                        {"subject_direction": direction},
                        {"entry_keywords": keywords}
                    ],
                    "event": event,
                   })
        elif isinstance(contain_descs, list):
            for contain_desc in contain_descs:
                event_desc = {}
                event_desc["logic"] = "and"
                condition = []
                condition.append({"subject_direction": direction})
                if only:
                    condition.append({"same_subjects_only_one":True})
                opposite = contain_desc["opposite"]
                if opposite != "all":
                    condition.append({"opposite_subjects": opposite})
                event_desc["condition"] = condition
                event = contain_desc["event"]
                event_desc["event"] = event
                problem = contain_desc["problem"]
                if problem != None:
                    event_desc["problem"] = problem
                item["judge"].append(event_desc)
        else:
            raise Exception("出错了")
        if isinstance(not_contain_descs, str):
            event = not_contain_descs
            if only:
                item["judge"].append({
                    "logic": "and",
                    "condition": [
                        {"subject_direction": direction},
                        {"same_subjects_only_one": True},
                        {"entry_keywords": keywords}
                    ],
                    "event": event,
                    })
            else:
                item["judge"].append({
                    "logic": "and",
                    "condition": [
                        {"subject_direction": direction},
                        {"entry_keywords": keywords}
                    ],
                    "event": event,
                    })
        elif isinstance(not_contain_descs, list):
            for not_contain_desc in not_contain_descs:
                event_desc = {}
                event_desc["logic"] = "and"
                condition = []
                condition.append({"subject_direction": direction})
                if only:
                    condition.append({"same_subjects_only_one": True})
                opposite = not_contain_desc["opposite"]
                if opposite != "all":
                    condition.append({"opposite_subjects": opposite})
                event_desc["condition"] = condition
                event = not_contain_desc["event"]
                event_desc["event"] = event
                problem = not_contain_desc["problem"]
                if problem != None:
                    event_desc["problem"] = problem
                item["judge"].append(event_desc)
        else:
            raise Exception("出错了")
    elif isinstance(direction_descs, list):
        # 判断是否为包含关键词的dict
        if "keywords" in direction_descs[0]:
            # 根据凭证中包含的关键词判断凭证性质
            for direction_desc in direction_descs:
                event_desc = {}
                event_desc["logic"] = "and"
                condition = []
                condition.append({"subject_direction": direction})
                if only:
                    condition.append({"same_subjects_only_one": True})
                keywords = direction_desc["keywords"]
                condition.append({"entry_keywords": keywords})
                event_desc["condition"] = condition
                event = direction_desc["contain_event"]
                event_desc["event"] = event
                problem = direction_desc["problem"]
                if problem != None:
                    event_desc["problem"] = problem
                item["judge"].append(event_desc)
        elif "opposite" in direction_descs[0]:
            # 根据对方会计科目判断凭证性质
            for direction_desc in direction_descs:
                event_desc = {}
                event_desc["logic"] = "and"
                condition = []
                condition.append({"subject_direction": direction})
                if only:
                    condition.append({"same_subjects_only_one": True})
                opposite = direction_desc["opposite"]
                if opposite != "all":
                    condition.append({"opposite_subjects": opposite})
                event_desc["condition"] = condition
                event = direction_desc["event"]
                event_desc["event"] = event
                problem = direction_desc["problem"]
                if problem != None:
                    event_desc["problem"] = problem
                item["judge"].append(event_desc)
    return item

res = []
for subject_desc in subject_descs:
    subject = subject_desc["subject"]
    no = subject_desc["no"]
    debit_only_one = subject_desc["debit_only_one"]
    credit_only_one = subject_desc["credit_only_one"]
    debit = subject_desc.get("debit",False)
    credit = subject_desc.get("credit",False)
    two_way = subject_desc.get("two_way",False)
    item = {}
    item["no"] = no
    item["subject"] = subject
    item["judge"] = []

    if debit:
        item = handle_desc(debit,item,debit_only_one,direction="借方")
    if credit:
        item = handle_desc(credit,item,credit_only_one,direction="贷方")
    if two_way:
        item = handle_desc(two_way,item,False,direction="双向")
    res.append(item)

print(res)






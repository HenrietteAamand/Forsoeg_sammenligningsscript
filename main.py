import filereader, extract_hrmpro, extract_maxrefdes103, tidskorrigering

path = "C:/Users/hah/Documents/VISUAL_STUDIO_CODE/Forsoeg_sammenligningsscript/Data"
fr = filereader.filereader_class(path=path)
tk = tidskorrigering.tidskorrigering_class(1635761570409,63780218)
hrm_pro = extract_hrmpro.extract_hrmpro_class(fr,tk)
maxrefdes103 = extract_maxrefdes103.extract_maxrefdes103_class(fr)


antal_testpersoner = 1
counter = 1
fasenummer = 1
while(counter <=antal_testpersoner):
    testpersonnummer = counter
    maxrefdes103.extract(testpersonnummer,fasenummer)
    timelim_begin = maxrefdes103.get_first_timestamp()
    timelim_end = maxrefdes103.get_last_timestamp()
    hrm_pro.extract(testpersonnummer,timelim_begin=timelim_begin, timelim_end=timelim_end)
    fasenummer += 1
    if(fasenummer > 3):
        counter += 1
        fasenummer = 1
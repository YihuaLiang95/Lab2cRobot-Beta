import re

#argument
command = "test command"
command_name = "测试命令"
command_list = command.split(' ')


#file1: cmd_word_params.yaml
with open('cmd_word_params.yaml',"rt",encoding = 'utf-8') as f:
    content=f.readlines()
    tab_record = -1
    i_record = -1
    for i in range(len(content)):
        #print(content[i])
        if command in content[i]:
            print("command exit")
            quit()
        if command_name in content[i]:
            print("command name exit")
            quit()
        tab=re.search('hello_world: 下午好',content[i])
        if tab!= None:
            tab_record = tab.end()
            i_record = i
    f.close()

    insert=''
    for string in command_list[:-1]:
        insert = insert+string+'_'
    insert = insert+command_list[-1]+": "+command_name+"\n"
    with open("cmd_word_params1.yaml","wt") as f:
        content=content[:i_record]+[insert]+content[i_record:]
        f.writelines(content)
        f.close()

        
#file2: tuling_nlu.cpp
with open('tuling_nlu.cpp',"rt") as f:
    content=f.readlines()
    tab_record = -1
    i_record = -1
    for i in range(len(content)):
        #print(content[i])
        tab=re.search('static string hello_world_str;',content[i])
        if tab!= None:
            tab_record = tab.end()
            i_record = i
    f.close()

    insert='static string '
    for string in command_list[:-1]:
        insert = insert+string+'_'
    insert = insert+command_list[-1]+"_str;\n"
    with open("tuling_nlu1.cpp","wt") as f:
        content=content[:i_record]+[insert]+content[i_record:]
        f.writelines(content)
        f.close()

with open('tuling_nlu1.cpp',"rt") as f:
    content=f.readlines()
    tab_record = -1
    i_record = -1
    number_record = -1
    for i in range(len(content)):
        #print(content[i])
        tab=re.search('#define NUMBER RECORD ',content[i])
        if tab!= None:
            number_record = int(re.findall(r'(?<=#define NUMBER RECORD )\d+', content[i])[0])
            tab_record = tab.end()
            i_record = i
            content[i] = content[i][:-3]+str(number_record+1)+'\n'
        tab_record = -1
        i_record = -1
    for i in range(len(content)):
        #print(content[i])
        tab=re.search('#define HELLO_WORLD_CMD 18',content[i])
        if tab!= None:
            tab_record = tab.end()
            i_record = i+1

    insert='#define '
    for string in command_list[:-1]:
        insert = insert+string.upper()+'_'
    insert = insert+command_list[-1].upper()+"_CMD "+str(number_record)+"\n"
    with open("tuling_nlu1.cpp","wt") as f:
        content=content[:i_record]+[insert]+content[i_record:]
        f.writelines(content)
        f.close()
        
with open('tuling_nlu1.cpp',"rt") as f:
    content=f.readlines()
    tab_record = -1
    i_record = -1
    for i in range(len(content)):
        tab=re.search('wstring helloWorldStr',content[i])
        if tab!= None:
            tab_record = tab.end()
            i_record = i
    f.close()

    insert='    wstring '+command_list[0]
    for string in command_list[1:]:
        insert = insert+string.capitalize()
    insert = insert+"Str = str2wstr("
    for string in command_list:
        insert = insert + string+"_"
    insert = insert+"str);\n"
    with open("tuling_nlu1.cpp","wt") as f:
        content=content[:i_record]+[insert]+content[i_record:]
        f.writelines(content)
        f.close()

with open('tuling_nlu1.cpp',"rt") as f:
    content=f.readlines()
    tab_record = -1
    i_record = -1
    for i in range(len(content)):
        if 'find(helloWorldStr)' in content[i]:
            i_record = i
    f.close()

    insert=[]
    insert_item = '    else if(convertStr.find('+command_list[0]
    for string in command_list[1:]:
        insert_item = insert_item+string.capitalize()
    insert_item=insert_item+'Str) != string::npos)\n'
    insert.append(insert_item)
    insert.append('    {\n')
    insert_item = '        ret = '
    for string in command_list:
        insert_item = insert_item+string.upper()+'_'
    insert_item = insert_item+'CMD;\n'
    insert.append(insert_item)
    insert.append('    }\n')
    with open("tuling_nlu1.cpp","wt") as f:
        content=content[:i_record]+insert+content[i_record:]
        f.writelines(content)
        f.close()
        
with open('tuling_nlu1.cpp',"rt") as f:
    content=f.readlines()
    i_record = -1
    for i in range(len(content)):
        if 'get("~hello_world", hello_world_str);' in content[i]:
            i_record = i
    f.close()

    insert = '    ros::param::get("~'
    for string in command_list[:-1]:
        insert = insert+string+'_'
    insert = insert+command_list[-1]+'", '
    for string in command_list:
        insert = insert+string+'_'
    insert = insert+'str);\n'
    with open("tuling_nlu1.cpp","wt") as f:
        content=content[:i_record]+[insert]+content[i_record:]
        f.writelines(content)
        f.close()
        
# file3 voice_move.cpp
with open('voice_move.cpp',"rt") as f:
    content=f.readlines()
    i_record = -1
    number_record = -1
    for i in range(len(content)):
        tab=re.search('#define NUMBER RECORD ',content[i])
        if tab!= None:
            number_record = int(re.findall(r'(?<=#define NUMBER RECORD )\d+', content[i])[0])
            i_record = i
            content[i] = content[i][:-3]+str(number_record+1)+'\n'
        i_record = -1
    for i in range(len(content)):
        tab=re.search('#define  HELLO_WORLD_CMD  18',content[i])
        if tab!= None:
            i_record = i+1

    insert='#define '
    for string in command_list[:-1]:
        insert = insert+string.upper()+'_'
    insert = insert+command_list[-1].upper()+"_CMD "+str(number_record)+"\n"
    with open("voice_move1.cpp","wt") as f:
        content=content[:i_record]+[insert]+content[i_record:]
        f.writelines(content)
        f.close()
        
with open('voice_move1.cpp',"rt") as f:
    content=f.readlines()
    i_record = -1
    for i in range(len(content)):
        if 'case HELLO_WORLD_CMD:' in content[i]:
            i_record = i
    f.close()

    insert = []
    insert_item = '    case '
    for string in command_list:
        insert_item = insert_item+string.upper()+'_'
    insert_item = insert_item+'CMD:\n'
    insert.append(insert_item)
    insert.append('            {\n')
    insert_item = '                nav_msg.data = "'
    for string in command_list[:-1]:
        insert_item = insert_item+string+' '
    insert_item = insert_item+command_list[-1]+'";\n'
    insert.append(insert_item)
    insert.append('                break;\n')
    insert.append('            }\n')
    with open("voice_move1.cpp","wt") as f:
        content=content[:i_record]+insert+content[i_record:]
        f.writelines(content)
        f.close()
        
#file 4 riki_patrol_nav.py
with open('riki_patrol_nav.py',"rt") as f:
    content=f.readlines()
    i_record = -1
    for i in range(len(content)):
        if 'elif self.nav_command == "hello world":' in content[i]:
            i_record = i
    f.close()

    insert = []
    insert_item = '                elif self.nav_command == "'
    for string in command_list[:-1]:
        insert_item = insert_item+string+' '
    insert_item = insert_item+command_list[-1]+'":\n'
    insert.append(insert_item)
    insert.append('\n')
    insert_item = '                    self.nav_command = ""\n'
    insert.append(insert_item)
    with open("riki_patrol_nav1.py","wt") as f:
        content=content[:i_record]+insert+content[i_record:]
        f.writelines(content)
        f.close()
        
with open('riki_patrol_nav1.py',"rt") as f:
    content=f.readlines()
    i_record = -1
    for i in range(len(content)):
        if "elif command == 'hello world':" in content[i]:
            i_record = i
    f.close()

    insert = []
    insert_item = "        elif command == '"
    for string in command_list[:-1]:
        insert_item = insert_item+string+' '
    insert_item = insert_item+command_list[-1]+"':\n"
    insert.append(insert_item)
    insert_item = "            self.nav_command = '"
    for string in command_list[:-1]:
        insert_item = insert_item+string+' '
    insert_item = insert_item+command_list[-1]+"'\n"
    insert.append(insert_item)
    insert.append('            return\n')
    with open("riki_patrol_nav1.py","wt") as f:
        content=content[:i_record]+insert+content[i_record:]
        f.writelines(content)
        f.close()
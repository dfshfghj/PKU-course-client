from .course_requests import Client
from bs4 import BeautifulSoup
import re
import os
import hashlib
from urllib.parse import urlparse, parse_qs


def uri2id(uri):
    pattern = r'(\w+_id)=([0123456789_]*)'
    matches = re.findall(pattern, uri)
    id_dict = {key: value for key, value in matches}
    return id_dict

def getPageTitle(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', {'id': 'pageTitleDiv'}).find('span').get_text(strip=True)

def getPortal(html):
    soup = BeautifulSoup(html, 'html.parser')
    portlets = soup.find_all('div', class_='portlet clearfix')
    current_courses = []
    history_courses = []
    for portlet in portlets:
        title = portlet.find('span', {'class': 'moduleTitle'}).get_text()
        controlWrappers = portlet.find_all('div', {'class': 'moduleControlWrapper u_reverseAlign'})
        for controlWrapper in controlWrappers:
            controlWrapper['style'] = "text-align: right;"
        if '当前学期课程' in title:
            for li in portlet.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    course_name = a_tag.get_text()
                    course_link = a_tag['href']
                    match = re.search(r'key=_([^,]+)', course_link)
                    if match:
                        key = match.group(1)
                        current_courses.append(
                            {'name': course_name, 'key': key})
        elif '历史课程' in title:
            for li in portlet.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    course_name = a_tag.get_text()
                    course_link = a_tag['href']
                    match = re.search(r'key=_([^,]+)', course_link)
                    if match:
                        key = match.group(1)
                        history_courses.append(
                            {'name': course_name, 'key': key})
        elif '我的公告' in title:
            announcement = portlet.find('div', {'class': 'collapsible'})
            announcement['style'] = "line-height: 2;"
            for h3 in announcement.find_all('h3'):
                h4 = soup.new_tag('h4')
                h4.string = h3.get_text()
                #h4['style'] = "font-size: 9px; font-weight: normal;"
                h3.replace_with(h4)
            # for a in announcement.find_all('a'):
            #     a['style'] = "color: none;"
        elif '我的组织' in title:
            organization = portlet.find('div', {'class': 'collapsible'})
            organization['style'] = "line-height: 2;"
            for h3 in organization.find_all('h3'):
                div = soup.new_tag('div')
                div.string = h3.get_text()
                h3.replace_with(div)
            # for a in organization.find_all('a'):
            #     a['style'] = "color: none;"
        elif '我的任务' in title:
            task = portlet.find('div', {'class': 'collapsible'})
            task['style'] = "line-height: 2;"
            for h3 in task.find_all('h3'):
                div = soup.new_tag('div')
                div.string = h3.get_text()
                h3.replace_with(div)
            # for a in task.find_all('a'):
            #     a['style'] = "color: none;"
    return current_courses, history_courses, str(announcement), str(organization), str(task)


def simplifyCourseName(course_name):
    return re.sub(r'^.*?: ', '', course_name).strip()


def getCourseAnnouncement(html, client=None):
    soup = BeautifulSoup(html, 'html.parser')
    announcement_list = soup.find('ul', {'id': 'announcementList'})
    get_announcements = []
    if announcement_list:
        announcements = announcement_list.find_all('li', {'class': 'clearfix'})
    else:
        return get_announcements
    for announcement in announcements:
        title = announcement.find('h3').get_text(strip=True)
        time_tag = announcement.find('div', {'class': 'details'}).find('p')
        post_time = time_tag.get_text(strip=True).split(':')[-1].strip()
        imgs = announcement.find_all('img')
        for img in imgs:
            src = img['src']
            if client:
                print('get image')
                response = client.get_by_uri(src, stream=True)
                response.raise_for_status()
                if response.status_code == 200:
                    image_format = response.url.split(".")[-1]
                    print(repr(response.url), hashlib.md5(response.url.encode()).hexdigest())
                    with open(os.path.join('data', 'cache', f'{hashlib.md5(response.url.encode()).hexdigest()}.{image_format}'), mode='wb') as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = os.path.abspath(temp_file.name)
                    img['src'] = f"file:///{temp_file_path}"
                else:
                    print('failed loading image')
            img['style'] = "max-width: 100%;"
        content_div = announcement.find('div', class_='vtbegenerated')
        content = str(content_div) if content_div else ''

        announcement_info_div = announcement.find(
            'div', class_='announcementInfo')
        poster, posted_to = list(map(lambda p: p.text.split(":")[-1].strip(), announcement_info_div.find_all('p')))
        get_announcements.append({'title': title, 'time': post_time,
                                 'poster': poster, 'post_to': posted_to, 'content': content})
        
        
    return get_announcements


def getCourseMenu(html):
    soup = BeautifulSoup(html, 'html.parser')
    menu_wrap = soup.find('div', {'id': 'menuWrap'})
    course_menu = menu_wrap.find('div', {'id': 'courseMenuPalette'})
    course_name = course_menu.find(
        'a', {'id': 'courseMenu_link'}).get_text(strip=True)
    menu_info = {'name': course_name,
                 'buttons': {},
                 'groups': []
                 }
    nav_buttons = course_menu.find(
        'ul', {'id': 'courseMenuPalette_contents'}).find_all('a')
    for nav_button in nav_buttons:
        href_url = nav_button['href']
        text = nav_button.get_text(strip=True)
        menu_info['buttons'][text] = href_url
    my_groups = menu_wrap.find('div', {'id': 'myGroups'}).find(
        'ul', {'id': 'myGroups_contents'}).find_all('li', recursive=False)
    for group in my_groups:
        menu_info['groups'].append(group.find(
            'h4', {'role': 'presentation'}).text)
    return menu_info


def getCourseDocuments(html):
    soup = BeautifulSoup(html, 'html.parser')
    contentList = soup.find_all('li', {'class': 'clearfix liItem read'})
    documents = []
    for content in contentList:
        img_alt = content.find('img')['alt']
        item = content.find('div', {'class': 'item clearfix'})
        name = ''
        a = item.find('a')
        if a:
            href = a['href']
            name = a.find('span').text
        else:
            href = ''
            for span in item.find_all('span'):
                if span.get_text(strip=True):
                    name = span.get_text(strip=True)
                    break
        details = content.find('div', {'class': 'details'})
        if details and details.get_text(strip=True):
            for element in details.find_all(True):
                if not ''.join(element.stripped_strings):
                    element.decompose()
            details = str(details)
        else:
            details = None
        documents.append({
            'href': href,
            'image': img_alt,
            'name': name,
            'details': details # ,
            #'appendix': appendix
        })
    return documents


def getTable(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    table = soup.find('div', {'class': 'container clearfix'}).find('table')
    thead = table.find('thead')
    heads = thead.find('tr').find_all('th')
    data.append([head.text for head in heads])
    trows = table.find('tbody').find_all('tr')
    for trow in trows:
        data.append([trow.find('th').text] + list(map(lambda x: str(x.find('span',
                    {'class': 'table-data-cell-value'})).replace('\n', ''), trow.find_all('td'))))
    return data

def getTables(html):
    soup = BeautifulSoup(html, 'html.parser')
    datas = []
    tables = soup.find('div', {'class': 'container clearfix'}).find_all('table')
    for table in tables:
        data = []
        thead = table.find('thead')
        heads = thead.find('tr').find_all('th')
        data.append([head.text for head in heads])
        trows = table.find('tbody').find_all('tr')
        for trow in trows:
            data.append([trow.find('th').text] + list(map(lambda x: str(x.find('span',
                        {'class': 'table-data-cell-value'})).replace('\n', ''), trow.find_all('td'))))
        datas.append(data)
    return datas

def getGradeTable(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    table = soup.find('div', {'class': 'container clearfix'}).find('div', {'role': 'table'})
    grades = table.find_all('span', {'class': 'grade'})
    for grade in grades:
        div = soup.new_tag('div')
        div.string = grade.get_text()
        div['style'] = "color: #0da5aa; font-weight: bold; font-size: 20px"
        grade.replace_with(div)
    grade_cells = table.find_all('div', {'class': 'cell grade'})
    for grade_cell in grade_cells:
        grade_cell['style'] = "text-align: right;"
    assignment_cells = table.find_all('div', {'class': 'cell gradable'})
    for assignment_cell in assignment_cells:
        assignment_name = assignment_cell.find('a')
        if assignment_name:
            assignment_name['style'] = "font-size: 16px; font-weight: bold; color: #3491fa;"
        else:
            assignment_name = assignment_cell.find('span')
            if assignment_name:
                assignment_name['style'] = "font-size: 16px; font-weight: bold;"
    total_points = table.find_all('span', {'class': 'pointsPossible clearfloats'})
    for total_point in total_points:
        div = soup.new_tag('div')
        div.string = total_point.get_text()
        total_point.replace_with(div)

    thead = table.find('div', {'class': 'grades_header'})
    heads = thead.find_all('div')
    data.append([head.text for head in heads])
    trows = table.find('div', {'id': 'grades_wrapper', 'role': 'rowgroup'}).find_all('div', recursive=False)
    for trow in trows:
        data.append(list(map(str, trow.find_all('div', {'role': 'cell'}))))
    return data

def getVideoInfo(html):
    soup = BeautifulSoup(html, 'html.parser')
    src = soup.find('div', {'class': 'container clearfix'}).find('iframe')['src']
    return src

def url2videoInfo(url):
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query)
    course_id = params.get('course_id', [None])[0]
    sub_id = params.get('sub_id', [None])[0]
    app_id = params.get('app_id', [None])[0]
    auth_data = params.get('auth_data', [None])[0]
    return course_id, sub_id, app_id, auth_data
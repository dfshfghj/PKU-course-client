from .course_requests import Client
from bs4 import BeautifulSoup
import re

def getCourseList(html):
    soup = BeautifulSoup(html, 'html.parser')
    portlets = soup.find_all('div', class_='portlet clearfix')
    current_courses = []
    history_courses = []
    for portlet in portlets:
        title = portlet.find('span', class_='moduleTitle').get_text()
        if '当前学期课程' in title:
            for li in portlet.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    course_name = a_tag.get_text()
                    course_link = a_tag['href']
                    match = re.search(r'key=_([^,]+)', course_link)
                    if match:
                        key = match.group(1)
                        current_courses.append({'name': course_name, 'key': key})
        elif '历史课程' in title:
            for li in portlet.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    course_name = a_tag.get_text()
                    course_link = a_tag['href']
                    match = re.search(r'key=_([^,]+)', course_link)
                    if match:
                        key = match.group(1)
                        history_courses.append({'name': course_name, 'key': key})
        elif '我的公告' in title:
            pass
    return current_courses, history_courses

def simplifyCourseName(course_name):
    return re.sub(r'^.*?: ', '', course_name).strip()

def getCourseAnnouncement(html):
    soup = BeautifulSoup(html, 'html.parser')
    announcement_list = soup.find('ul', {'id': 'announcementList'})
    get_announcements = []
    if announcement_list:
        announcements = announcement_list.find_all('li')
    else:
        return get_announcements
    for announcement in announcements:
        title = announcement.find('h3').get_text(strip=True)
        time_tag = announcement.find('p', text=lambda t: t and "发布时间:" in t)
        post_time = time_tag.get_text(strip=True).replace("发布时间:", "")

        content_div = announcement.find('div', class_='vtbegenerated')
        content = str(content_div) if content_div else ''
        
        announcement_info_div = announcement.find('div', class_='announcementInfo')
        for p in announcement_info_div.find_all('p'):
            if "发帖者:" in p.text:
                poster = p.text.replace("发帖者:", "").strip()
            elif "发布至:" in p.text:
                posted_to = p.text.replace("发布至:", "").strip()
        get_announcements.append({'title': title, 'time': post_time, 'poster': poster, 'post_to': posted_to, 'content': content})
    return get_announcements

def getCourseMenu(html):
    soup = BeautifulSoup(html, 'html.parser')
    menu_wrap = soup.find('div', {'id': 'menuWrap'})
    course_menu = menu_wrap.find('div', {'id': 'courseMenuPalette'})
    course_name = course_menu.find('a', {'id': 'courseMenu_link'}).get_text(strip=True)
    menu_info = {'name': course_name,
                 'buttons': [],
                 'urls': {},
                 'groups': []
    }
    nav_buttons = course_menu.find('ul', {'id': 'courseMenuPalette_contents'}).find_all('a')
    for nav_button in nav_buttons:
        href_url = nav_button['href']
        text = nav_button.text
        menu_info['buttons'].append(text)
        menu_info['urls'][text] = href_url
    my_groups = menu_wrap.find('div', {'id': 'myGroups'}).find('ul', {'id': 'myGroups_contents'}).find_all('li', recursive=False)
    for group in my_groups:
        menu_info['groups'].append(group.find('h4', {'role': 'presentation'}).text)
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
            'details': details
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
        data.append([trow.find('th').text] + list(map(lambda x: str(x.find('span', {'class': 'table-data-cell-value'})).replace('\n', ''), trow.find_all('td'))))
    return data



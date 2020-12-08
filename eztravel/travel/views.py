from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from .models import Post
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from travel import Using_Saved_Model
import pandas as pd
import random, json, pymysql
pymysql.install_as_MySQLdb()

# Create your views here.
class mainview(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        context = {
            'user': request.user.username,
            'default': True,
        }
        return render(request, 'travel/index.html', context)

def index(request):
    return render(request, 'travel/index.html')

def know(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')
    context = {
        'posts': posts,
    } 
    return render(request, 'travel/know.html', context)

def know_show(request, pk):
    post = Post.objects.get(pk=pk)
    context={
        'post':post
    }
    return render(request, 'travel/know_show.html', context)

def howto(request):
    return render(request, 'travel/howto.html')

def login(request):
    return render(request, 'travel/login.html')

class PostTemplateView(TemplateView):
    template_name = 'travel/loading.html'

def uimage(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)  # 이미지르 업로드할때 쓰는 form
        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()  # 이미지 파일을 저장
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = "{}".format(myfile)
            img_path = 'C:/Users/songtg/Desktop/Final_project/eztravel/media/' + uploaded_file_url
            print(uploaded_file_url)
            result = Using_Saved_Model.execute_model(img_path)
            print(result)
            file_url=fs.url(filename)
            context = {
                'result' : result,
                'uploaded_file_url' : img_path
            }
            print(type(context))
            print(context['result'])
            return JsonResponse({"result":result, "file_url":file_url})
            #return render(request, 'travel/uimage.html', context)
    else:
        form = UploadImageForm()
        print(form, "----------------------------------------------------------------------")
        return render(request, 'travel/uimage.html', {'form': form})

def getmap(request):
    print('upload page 시작')
    if request.method == 'POST':
        text=request.POST['result_data']
    print("status: ", text)


    # db에서 모든 table 정보를 list 형태로 가져옴
    db_info = get_db()
    
    # 명소
    #attraction_list = pd.read_csv('C:/Users/songtg/Desktop/Final_project/eztravel/data_file/new_attraction.csv')
    attraction_list = pd.DataFrame(db_info[0])
    attraction_list.columns = ['name', 'location', 'y', 'x', 'area']

    # 맛집
    # restaurant_list = pd.read_csv('C:/Users/songtg/Desktop/Final_project/eztravel/data_file/new_restaurant.csv')
    restaurant_list = pd.DataFrame(db_info[2])
    restaurant_list.columns = ['name', 'menu', 'location', 'y', 'x', 'area', 'phone', 'time', 'star']

    # 포토존
    # photozone_list = pd.read_csv('C:/Users/songtg/Desktop/Final_project/eztravel/data_file/new_photozone.csv')
    photozone_list = pd.DataFrame(db_info[1])
    photozone_list.columns = ['name', 'location', 'y', 'x', 'area']

    # 명소의 좌표
    attraction = attraction_list[attraction_list['name'] == map_name(text)]
    location_x = attraction['x'].tolist()
    location_y = attraction['y'].tolist()
    attr = attraction['name'].tolist()[0]
    print('attr', attr)
    # 명소와 같은 지역을 찾는 것
    region = attraction['area'].tolist()[0]
    print('region', region)

    # 맵에 찍힌 명소와 주소 상 같은 지역인 맛집만을 알려주기 위해
    rest_info = restaurant_list[restaurant_list['area'] == region][:4]
    rest_info_x = rest_info['x'].tolist()
    rest_info_y = rest_info['y'].tolist()
    rest_info_name = rest_info['name'].tolist()
    # print(len(rest_info_x), len(rest_info_y), len(rest_info_name))
    rest_info_phone = rest_info['phone'].tolist()
    rest_info_time = rest_info['time'].tolist()
    rest_info_star = rest_info['star'].tolist()
    rest_info_menu = rest_info['menu'].tolist()
    # 위와 같이 맵에 찍힌 명소와 같은 지경의 포토존을 추천해주기 위해
    photo_info = photozone_list[photozone_list['area'] == region][:3]
    photo_info_x = photo_info['x'].tolist()
    photo_info_y = photo_info['y'].tolist()
    photo_info_name = photo_info['name'].tolist()
    # print(len(rest_info_x), len(rest_info_y), len(rest_info_name))

    context = {
        'y' : location_y,
        'x' : location_x,
        'name' : attr,
        'x_rest' : rest_info_x,
        'y_rest' : rest_info_y,
        'n_rest' : rest_info_name,
        'p_rest' : rest_info_phone,
        't_rest' : rest_info_time,
        's_rest' : rest_info_star,
        'm_rest' : rest_info_menu,
        'x_photo' : photo_info_x,
        'y_photo' : photo_info_y,
        'n_photo' : photo_info_name,
    }

    return render(request, 'travel/tmap.html', context)


result_dict = {
    'Skybay': '스카이베이',
    'SunCruise': '썬크루즈리조트엔호텔',
    ' Gwangandaegyo': '광안대교',
    '5.18Park': '5.18 기념공원',
    'GwanghwamunSquare': '광화문광장',
    'NamsanTower': '남산서울타워',
    'DaejeonExpo': '엑스포과학공원',
    'D_Ark': '디아크문화관',
    'LotteWorldTower': '롯데월드타워',
    'MetasequoiaRoad': '하늘공원 메타세콰이어길',
    'Seokgulam': '석굴암',
    'Anapji': '안압지',
    'Yongdu.MtTower': '부산타워',
    'UlsanPostbox': '소망우체통',
    'UlsanBigwheel': '롯데꿈동산 공중관람차',
    'UlsanBridge': '울산대교',
    'Waterpoly': '워터폴리',
    'ChinaTown': '인천차이나타운',
    'Tryball': '트라이보울',
    'JagalchiMarket': '자갈치시장',
    'IndependenceHall': '독립기념관',
    'Cheomseongdae': '첨성대',
    'HomiPoint': '호미곶'
}

def map_name(model_result):
    map_name = result_dict[model_result]
    return map_name

# def place_info(request):
    # return render(request, 'travel/place_info.html')

def get_db():
    mysql = pymysql.connect(
        user='admin',
        db='final_db',
        passwd='adminmysql',
        host='database-1.c9jk87ku5jbk.us-east-1.rds.amazonaws.com',
        charset='utf8',
    )
    cursor = mysql.cursor()

    # DB에 존자하는 테이블 보기
    sql = "show tables;"
    cursor.execute(sql)
    tables = cursor.fetchall()
    print(tables)

    # 테이블에 저장된 정보 보기
    table_info = []
    for table in tables:
        cmd = "SELECT * FROM {}".format(table[0])
        print(cmd)
        
        cursor.execute(cmd)
        info = list(cursor.fetchall())
        table_info.append(info)

    return table_info
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from .models import Post
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from travel import Using_Saved_Model, recommendation
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
            result = map_name(result)
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
    restaurant_list = pd.DataFrame(db_info[3])
    restaurant_list.columns = ['name', 'menu', 'location', 'y', 'x', 'area', 'phone', 'time', 'star']

    # 포토존
    # photozone_list = pd.read_csv('C:/Users/songtg/Desktop/Final_project/eztravel/data_file/new_photozone.csv')
    photozone_list = pd.DataFrame(db_info[1])
    photozone_list.columns = ['name', 'location', 'y', 'x', 'area']

    # 명소의 좌표
    attraction = attraction_list[attraction_list['name'] == text]
    location_x = attraction['x'].tolist()
    location_y = attraction['y'].tolist()
    attr = attraction['name'].tolist()[0]
    print('attr', attr)
    # global rec_attr
    # rec_attr = attr

    # 명소와 같은 지역을 찾는 것
    region = attraction['area'].tolist()[0]
    print('region', region)
    # global rec_region
    # rec_region = region

    # 명소와 가장 가까운 곳을 알려주기 위해
    r_sorted_list = []
    for rest in restaurant_list[restaurant_list['area'] == region].values:
        y = abs(location_y[0] - rest[3])
        x = abs(location_x[0] - rest[4])
        r_sorted_list.append([x+y, rest.tolist()])
    r_sorted_list = sorted(r_sorted_list)

    new_r_list = []
    for i in r_sorted_list:
        new_r_list.append(i[1])
    new_restaurant_list = pd.DataFrame(new_r_list, columns = ['name', 'menu', 'location', 'y', 'x', 'area', 'phone', 'time', 'star'])

    p_sorted_list = []
    for rest in photozone_list[photozone_list['area'] == region].values:
        y = abs(location_y[0] - rest[2])
        x = abs(location_x[0] - rest[3])
        p_sorted_list.append([x+y, rest.tolist()])
    p_sorted_list = sorted(p_sorted_list)
    
    new_p_list = []
    for i in p_sorted_list:
        new_p_list.append(i[1])
    new_photozone_list = pd.DataFrame(new_p_list, columns = ['name', 'location', 'y', 'x', 'area'])


    # 맵에 찍힌 명소와 주소 상 같은 지역인 맛집만을 알려주기 위해
    rest_info = new_restaurant_list[new_restaurant_list['area'] == region][:4]
    rest_info_x = rest_info['x'].tolist()
    rest_info_y = rest_info['y'].tolist()
    rest_info_name = rest_info['name'].tolist()
    rest_info_phone = rest_info['phone'].tolist()
    rest_info_time = rest_info['time'].tolist()
    rest_info_star = rest_info['star'].tolist()
    rest_info_menu = rest_info['menu'].tolist()

    # 위와 같이 맵에 찍힌 명소와 같은 지경의 포토존을 추천해주기 위해
    photo_info = new_photozone_list[new_photozone_list['area'] == region][:3]
    photo_info_x = photo_info['x'].tolist()
    photo_info_y = photo_info['y'].tolist()
    photo_info_name = photo_info['name'].tolist()

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
        'attr': attr,
        'region': region,
    }

    return render(request, 'travel/tmap.html', context)

def recommend(request):
    if request.method == 'POST':
        print('post')
        rec_region=request.POST['region_data']
        rec_attr=request.POST['attr_data']
    print("지역: ", rec_region)
    print("명소: ", rec_attr)

    rec_route = recommendation.recommend_place(rec_region, rec_attr)
    rec_route.append(rec_attr)
    print('추천장소: ', rec_route)

    db = get_db()[2]
    df = pd.DataFrame(db, columns=['name', 'location', 'y', 'x', 'area'])

    y = []
    x = []
    for route in rec_route:
        y.append(df[df['name'] == route]['y'].values.tolist()[0])
        x.append(df[df['name'] == route]['x'].values.tolist()[0])
    dot_y = y[0]
    dot_x = x[0]
    print('좌표:',dot_y, dot_x)
    context = {
        'rec_route': rec_route,
        'y': y,
        'x': x,
        'dot_y': dot_y,
        'dot_x': dot_x,
    }

    return render(request, 'travel/recommend.html', context)

result_dict = {
    'Skybay': '스카이베이 경포',
    'SunCruise': '썬크루즈리조트엔호텔',
    'Gwangandaegyo': '광안대교',
    '5.18Park': '5.18 기념공원',
    'GwanghwamunSquare': '광화문광장',
    'NamsanTower': '남산서울타워',
    'DaejeonExpo': '엑스포과학공원 한빛탑',
    'D_Ark': '디아크문화관',
    'LotteWorldTower': '롯데월드타워',
    'MetasequoiaRoad': '메타세콰이아가로수길',
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
    'HomiPoint': '호미곶',
    "SamyangRanch":"대관령 삼양 목장",
    "Gangwonland":"강원랜드",
    "WawooTemple":"와우정사",
    "Panmunjeom":"판문점",
    "BoseongGreenteaFarm":"보성녹차밭",
    "SokchoExpoTower":"속초 엑스포 타워",
    "GreenCityObservatory":"송산그린시티전망대",
    "OdongIsletLightHouse":"여수오동도등대",
    "JeondongChurch":"전동성당",
    "GlassHouse":"글라스하우스",
    "BangjuChurch":"방주교회",
    "SeongisidolRanch":"성이시돌목장",
    "BeopjuTemple":"법주사",
    "SeokjoMaitreya":"석조미륵보살",
    "HapdeokChurch":"천주교 합덕 성당"
}

def map_name(model_result):
    map_name = result_dict[model_result]
    print(map_name)
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
    # commit 확인용
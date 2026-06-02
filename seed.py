from app import create_app, db
from app.models.user import User
from app.models.category import Category
from app.models.archive import Archive
from app.models.collection import Collection

app = create_app()


def seed():
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("数据库已有数据，跳过种子数据初始化")
            return

        admin = User(username="admin", display_name="管理员", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

        editor = User(username="editor", display_name="编辑员", role="editor")
        editor.set_password("editor123")
        db.session.add(editor)

        viewer = User(username="viewer", display_name="浏览者", role="viewer")
        viewer.set_password("viewer123")
        db.session.add(viewer)

        db.session.flush()

        categories_data = [
            {"name": "书法", "description": "中国书法艺术作品，涵盖历代名家碑帖、手卷等"},
            {"name": "绘画", "description": "中国传统绘画作品，包括山水、花鸟、人物画等"},
            {"name": "陶瓷", "description": "中国陶瓷器物，涵盖各朝代名窑精品"},
            {"name": "青铜器", "description": "中国古代青铜器，包括礼器、兵器、乐器等"},
            {"name": "织绣", "description": "中国织绣工艺品，包括丝织、刺绣、缂丝等"},
            {"name": "建筑", "description": "中国古建筑遗产，涵盖宫殿、寺庙、园林等"},
        ]
        category_map = {}
        for cat_data in categories_data:
            cat = Category(name=cat_data["name"], description=cat_data["description"])
            db.session.add(cat)
            category_map[cat_data["name"]] = cat

        db.session.flush()

        archives_data = [
            {
                "title": "兰亭集序",
                "description": "东晋书法家王羲之所作，被誉为"天下第一行书"。此帖笔法精妙，行气贯通，是中国书法艺术的巅峰之作。原迹已失传，现存多为唐人摹本，以冯承素摹本"神龙本"最为著名。",
                "category": "书法",
                "era": "东晋",
                "location": "浙江绍兴",
                "status": "published",
            },
            {
                "title": "祭侄文稿",
                "description": "唐代书法家颜真卿为祭奠在安史之乱中殉国的侄子颜季明所作。全篇气势磅礴，悲愤之情溢于笔端，被誉为"天下第二行书"。笔法沉着痛快，墨色枯润相间，情感真挚动人。",
                "category": "书法",
                "era": "唐代",
                "location": "陕西西安",
                "status": "published",
            },
            {
                "title": "寒食帖",
                "description": "北宋苏轼被贬黄州时所书，又称《黄州寒食诗帖》。笔法苍劲有力，结体跌宕起伏，被誉为"天下第三行书"。此帖充分体现了苏轼在逆境中的豁达与深沉。",
                "category": "书法",
                "era": "北宋",
                "location": "湖北黄州",
                "status": "published",
            },
            {
                "title": "千里江山图",
                "description": "北宋画家王希孟所作青绿山水长卷，描绘了祖国大好河山的壮丽景象。全卷以石青、石绿为主色，色彩绚丽而不失典雅，是中国青绿山水画的代表作。",
                "category": "绘画",
                "era": "北宋",
                "location": "北京故宫博物院",
                "status": "published",
            },
            {
                "title": "清明上河图",
                "description": "北宋画家张择端所作，描绘了北宋都城汴京的城市面貌和各阶层人民的生活状况。全卷长528.7厘米，宽24.8厘米，画面细节丰富，是中国风俗画的巅峰之作。",
                "category": "绘画",
                "era": "北宋",
                "location": "北京故宫博物院",
                "status": "published",
            },
            {
                "title": "富春山居图",
                "description": "元代画家黄公望所作水墨山水长卷，描绘了富春江两岸的秀丽景色。此画被誉为"画中之兰亭"，是中国文人画的代表作。后因火焚分为两段，分别藏于两岸。",
                "category": "绘画",
                "era": "元代",
                "location": "浙江富阳",
                "status": "published",
            },
            {
                "title": "汝窑天青釉洗",
                "description": "北宋汝窑代表作，釉色天青，温润如玉。汝窑为宋代五大名窑之首，传世品极少，此洗为存世精品之一。釉面开片细密，如冰裂纹，极具观赏价值。",
                "category": "陶瓷",
                "era": "北宋",
                "location": "河南宝丰",
                "status": "published",
            },
            {
                "title": "元青花鬼谷子下山图罐",
                "description": "元代青花瓷器的巅峰之作，罐身绘鬼谷子下山故事图。人物刻画生动，青花发色浓艳，构图疏密有致。2005年在伦敦佳士得拍卖会上以约2.3亿人民币成交，创当时中国艺术品拍卖纪录。",
                "category": "陶瓷",
                "era": "元代",
                "location": "江西景德镇",
                "status": "published",
            },
            {
                "title": "后母戊鼎",
                "description": "商代晚期青铜礼器，是中国已知最大最重的青铜器。鼎重832.84千克，高133厘米，造型庄严雄伟，纹饰精美。鼎腹内壁铸有"后母戊"三字，是商王为祭祀其母所铸。",
                "category": "青铜器",
                "era": "商代",
                "location": "河南安阳",
                "status": "published",
            },
            {
                "title": "四羊方尊",
                "description": "商代晚期青铜酒器，四角各铸一卷角羊头，造型奇特，工艺精湛。尊的肩部饰有龙纹，腹部饰有兽面纹，整体设计巧妙，是中国古代青铜器中的珍品。",
                "category": "青铜器",
                "era": "商代",
                "location": "湖南宁乡",
                "status": "published",
            },
            {
                "title": "素纱襌衣",
                "description": "西汉马王堆汉墓出土的丝织精品，整件衣服仅重49克，轻薄透明，体现了西汉高超的丝织技术。衣长128厘米，通袖长190厘米，是现存最早、最轻薄的衣服。",
                "category": "织绣",
                "era": "西汉",
                "location": "湖南长沙",
                "status": "published",
            },
            {
                "title": "缂丝牡丹图",
                "description": "南宋缂丝精品，以缂丝技法织造牡丹图案，色彩艳丽，层次分明。缂丝又称"刻丝"，是中国传统丝织工艺中最珍贵的一种，有"一寸缂丝一寸金"之说。",
                "category": "织绣",
                "era": "南宋",
                "location": "江苏苏州",
                "status": "published",
            },
            {
                "title": "应县木塔",
                "description": "全称佛宫寺释迦塔，位于山西省应县，建于辽清宁二年（1056年），是中国现存最古老最高的纯木结构楼阁式建筑。塔高67.31米，共九层，全塔无一根铁钉，堪称建筑奇迹。",
                "category": "建筑",
                "era": "辽代",
                "location": "山西应县",
                "status": "published",
            },
            {
                "title": "故宫太和殿",
                "description": "明清两代皇宫主殿，又称金銮殿，是中国现存最大的木结构大殿。殿高35.05米，面积2377平方米，是皇帝举行重大典礼的场所。建筑气势恢宏，装饰华丽精美。",
                "category": "建筑",
                "era": "明代",
                "location": "北京",
                "status": "draft",
            },
            {
                "title": "定窑白瓷孩儿枕",
                "description": "北宋定窑代表作，瓷枕塑成一个俯卧的孩儿形象，孩儿两臂交叉趴卧，双足翘起，神态天真可爱。釉色白中泛黄，温润如象牙，是定窑白瓷中的精品。",
                "category": "陶瓷",
                "era": "北宋",
                "location": "河北曲阳",
                "status": "archived",
            },
            {
                "title": "曾侯乙编钟",
                "description": "战国早期青铜乐器，1978年出土于湖北随州。全套编钟共65件，总重2567千克，音域跨五个半八度，能演奏完整的五声、七声音阶，是中国古代音乐文明的杰出代表。",
                "category": "青铜器",
                "era": "战国",
                "location": "湖北随州",
                "status": "published",
            },
        ]

        for a_data in archives_data:
            cat = category_map.get(a_data["category"])
            archive = Archive(
                title=a_data["title"],
                description=a_data["description"],
                category_id=cat.id if cat else None,
                era=a_data["era"],
                location=a_data["location"],
                status=a_data["status"],
                created_by=admin.id,
            )
            db.session.add(archive)

        collections_data = [
            {
                "name": "中国书法经典",
                "description": "收录中国书法史上最具代表性的经典作品，涵盖行书、楷书、草书等各体精品。",
            },
            {
                "name": "宋代艺术精华",
                "description": "汇集宋代各类艺术精品，包括绘画、陶瓷、书法等，展现宋代文化艺术的辉煌成就。",
            },
            {
                "name": "青铜文明",
                "description": "收录中国青铜时代的重要器物，展现商周至战国时期青铜铸造工艺的卓越成就。",
            },
            {
                "name": "丝路遗珍",
                "description": "收录与丝绸之路相关的文化遗产，展现东西方文明交流的历史印记。",
            },
        ]
        for c_data in collections_data:
            collection = Collection(
                name=c_data["name"],
                description=c_data["description"],
                created_by=admin.id,
            )
            db.session.add(collection)

        db.session.commit()

        all_archives = Archive.query.all()
        all_collections = Collection.query.all()

        if len(all_collections) >= 1 and len(all_archives) >= 3:
            calligraphy = [a for a in all_archives if a.category_id == category_map["书法"].id]
            for a in calligraphy:
                all_collections[0].archive_items.append(a)

        if len(all_collections) >= 2 and len(all_archives) >= 5:
            song_archives = [
                a for a in all_archives
                if a.era and "宋" in a.era
            ]
            for a in song_archives:
                all_collections[1].archive_items.append(a)

        if len(all_collections) >= 3 and len(all_archives) >= 5:
            bronze = [a for a in all_archives if a.category_id == category_map["青铜器"].id]
            for a in bronze:
                all_collections[2].archive_items.append(a)

        if len(all_collections) >= 4:
            silk_road = [a for a in all_archives if a.id in [1, 4, 5, 9, 13]]
            for a in silk_road:
                all_collections[3].archive_items.append(a)

        db.session.commit()
        print("种子数据初始化完成！")
        print("默认账号：admin/admin123, editor/editor123, viewer/viewer123")


if __name__ == "__main__":
    seed()

"""
测试数据填充脚本
在backend目录下运行: python scripts/seed_test_data.py
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.class_group import ClassGroup
from app.models.child import Child
from app.models.teacher import Teacher
from app.models.anecdote import Anecdote
from app.models.anecdote_child import AnecdoteChild
from app.models.assessment import Assessment, AssessmentReport


def seed():
    app = create_app()
    with app.app_context():
        # 清空现有数据
        print("清空现有数据...")
        AnecdoteChild.query.delete()
        Anecdote.query.delete()
        AssessmentReport.query.delete()
        Assessment.query.delete()
        Child.query.delete()
        Teacher.query.delete()
        ClassGroup.query.delete()
        db.session.commit()

        # ===== 1. 创建班级 =====
        print("创建班级...")
        class1 = ClassGroup(name="大一班", age_group="5-6岁", academic_year="2025-2026")
        class2 = ClassGroup(name="中一班", age_group="4-5岁", academic_year="2025-2026")
        db.session.add_all([class1, class2])
        db.session.commit()

        # ===== 2. 创建幼儿 =====
        print("创建幼儿...")
        children_c1 = [
            Child(name="张梓萱", gender="女", birth_date="2019-09-15", class_id=class1.id, notes="性格开朗，喜欢画画"),
            Child(name="李浩然", gender="男", birth_date="2019-11-03", class_id=class1.id, notes="活泼好动，喜欢建构区"),
            Child(name="王子墨", gender="男", birth_date="2020-01-20", class_id=class1.id, notes="安静内向，喜欢阅读"),
            Child(name="刘诗涵", gender="女", birth_date="2019-07-08", class_id=class1.id, notes="善于表达，喜欢角色扮演"),
            Child(name="陈宇轩", gender="男", birth_date="2020-03-12", class_id=class1.id, notes="好奇心强，喜欢科学区"),
            Child(name="赵雨桐", gender="女", birth_date="2019-12-25", class_id=class1.id, notes="乐于助人，喜欢帮助老师"),
            Child(name="孙一诺", gender="男", birth_date="2020-02-18", class_id=class1.id, notes="注意力集中，喜欢拼图"),
            Child(name="周欣怡", gender="女", birth_date="2019-10-05", class_id=class1.id, notes="想象力丰富，喜欢美工区"),
        ]
        children_c2 = [
            Child(name="黄梓豪", gender="男", birth_date="2020-06-10", class_id=class2.id, notes="喜欢户外活动"),
            Child(name="吴思颖", gender="女", birth_date="2020-08-22", class_id=class2.id, notes="语言表达清晰"),
            Child(name="郑博文", gender="男", birth_date="2020-05-14", class_id=class2.id, notes="喜欢听故事"),
            Child(name="林可馨", gender="女", birth_date="2020-09-30", class_id=class2.id, notes="喜欢音乐活动"),
            Child(name="杨子涵", gender="男", birth_date="2020-07-18", class_id=class2.id, notes="喜欢和同伴一起玩"),
        ]
        db.session.add_all(children_c1 + children_c2)
        db.session.commit()
        print(f"  大一班: {len(children_c1)}名幼儿")
        print(f"  中一班: {len(children_c2)}名幼儿")

        # ===== 3. 创建教师（从记录中自动提取） =====
        print("创建教师...")
        teachers = [
            Teacher(name="王老师"),
            Teacher(name="李老师"),
            Teacher(name="陈老师"),
        ]
        db.session.add_all(teachers)
        db.session.commit()

        # ===== 4. 创建轶事记录 =====
        print("创建轶事记录...")
        today = datetime.now()
        anecdotes_data = [
            # 大一的记录
            {
                "class_id": class1.id, "teacher_id": teachers[0].id,
                "location": "建构区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=0, hours=2),
                "content": "今天上午区域活动时间，张梓萱和李浩然一起在建构区搭建城堡。张梓萱负责设计城堡的外观，她用积木搭了一个很高的塔楼，还细心地在旁边放了两棵小树。李浩然则负责搭建城墙，他尝试了好几种方式才找到最稳固的搭建方法。两人合作得非常好，遇到分歧时能互相商量解决。王老师在旁边观察了大约20分钟，两个孩子全程保持了很高的专注力。",
                "children_names": ["张梓萱", "李浩然"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[0].id,
                "location": "阅读区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=0, hours=1),
                "content": "王子墨今天在阅读区看了一本关于恐龙的绘本，看了大约15分钟。刘诗涵走过来问他：\"你在看什么呀？\"王子墨指着书上的图片说：\"这是霸王龙，它的牙齿好长！\"刘诗涵说：\"我也想看，我们可以一起看吗？\"王子墨点了点头，两个人头靠头一起翻看绘本，偶尔还会讨论书上的内容。王老师注意到王子墨今天比平时更愿意和同伴交流。",
                "children_names": ["王子墨", "刘诗涵"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[1].id,
                "location": "户外操场", "activity_type": "户外活动",
                "observed_at": today - timedelta(days=1),
                "content": "李老师组织了户外体育游戏\"小兔过河\"。陈宇轩在跨跳环节表现得非常积极，第一次尝试时差点摔倒，但他没有放弃，连续试了三次终于成功跳过去了。他高兴地喊道：\"李老师你看，我跳过去了！\"赵雨桐在旁边给他鼓掌说：\"陈宇轩你真棒！\"孙一诺在平衡木上走得很稳，速度比上周快了很多。周欣怡在沙池旁边用模具做了好几个小动物，还给它们搭了一个小房子。",
                "children_names": ["陈宇轩", "赵雨桐", "孙一诺", "周欣怡"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[0].id,
                "location": "美工区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=2),
                "content": "张梓萱今天在美工区用彩泥做了一只小兔子。她先揉了一个圆球做身体，又做了两个长条做耳朵，最后用黑色彩泥做了眼睛。她对自己的作品很满意，拿去给周欣怡看。周欣怡说：\"你的兔子好可爱！我也想做一个。\"两个人一起在美工区创作了大约30分钟。张梓萱还主动帮周欣怡揉彩泥，两个人有说有笑的。",
                "children_names": ["张梓萱", "周欣怡"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[1].id,
                "location": "科学区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=3),
                "content": "陈宇轩今天在科学区用放大镜观察树叶。他非常仔细地比较了两片不同树叶的纹路，还让王老师帮他拍照记录。他说：\"王老师你看，这片叶子的纹路像小河一样，另一片像手掌。\"李浩然也跑过来看，两个孩子一起收集了五片不同的树叶，按大小排成一排。陈宇轩还尝试用画笔把叶子的纹路拓印到纸上，效果非常好。",
                "children_names": ["陈宇轩", "李浩然"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[2].id,
                "location": "集体教学", "activity_type": "集体教学",
                "observed_at": today - timedelta(days=4),
                "content": "陈老师今天组织了数学活动\"按规律排序\"。刘诗涵第一个完成了练习卡上的任务，她不仅能按颜色排序，还能发现更复杂的规律。王子墨在ABAB模式上有些困难，陈老师耐心地引导他用积木实际操作，经过三次练习后他终于理解了。赵雨桐主动帮助旁边有困难的同学，说：\"你先放红的，再放蓝的，就像这样。\"课堂氛围很活跃，大部分孩子都能完成基础任务。",
                "children_names": ["刘诗涵", "王子墨", "赵雨桐"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[0].id,
                "location": "角色区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=5),
                "content": "刘诗涵今天在角色区扮演\"小医生\"，她穿上白大褂，拿着听诊器给每个\"病人\"检查。张梓萱扮演\"护士\"，负责登记病人信息。李浩然来\"看病\"，刘诗涵问他：\"你哪里不舒服？\"李浩然说：\"我肚子疼。\"刘诗涵用听诊器听了听说：\"你要多喝热水，少吃冰激凌。\"孙一诺在旁边扮演\"药剂师\"，负责给\"病人\"拿药。整个角色扮演持续了约25分钟，孩子们的语言表达和社交能力都有很好的展现。",
                "children_names": ["刘诗涵", "张梓萱", "李浩然", "孙一诺"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[1].id,
                "location": "生活活动", "activity_type": "生活活动",
                "observed_at": today - timedelta(days=6),
                "content": "今天午餐时间，周欣怡主动帮李老师分发餐具，她数得很准确，每个桌子放四套。孙一诺吃饭时不太专心，东张西望，李老师轻轻提醒他：\"一诺，专心吃饭才能长高高哦。\"他马上认真吃起来。陈宇轩今天尝试自己盛汤，虽然手有点抖，但没有洒出来，他看起来很自豪。赵雨桐吃完后主动擦桌子，还帮旁边的小朋友擦了。",
                "children_names": ["周欣怡", "孙一诺", "陈宇轩", "赵雨桐"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[2].id,
                "location": "户外操场", "activity_type": "户外活动",
                "observed_at": today - timedelta(days=7),
                "content": "陈老师组织了\"老鹰捉小鸡\"的游戏。李浩然自告奋勇当老鹰，他跑得很快但注意不撞到其他小朋友。张梓萱当鸡妈妈，张开双臂保护身后的小朋友。王子墨一开始有点害羞，不太敢跑，但在刘诗涵的鼓励下也加入了游戏。游戏结束后，陈宇轩说：\"我下次想当老鹰！\"周欣怡和赵雨桐在旁边玩跳绳，周欣怡能连续跳五个，比上周多了两个。",
                "children_names": ["李浩然", "张梓萱", "王子墨", "刘诗涵", "陈宇轩", "周欣怡", "赵雨桐"],
            },
            {
                "class_id": class1.id, "teacher_id": teachers[0].id,
                "location": "建构区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=10),
                "content": "李浩然今天在建构区搭建了一个\"停车场\"。他先用大积木搭了围墙，然后在里面用小积木做了很多\"停车位\"。他一边搭一边自言自语：\"这里停小车，这里停大车。\"陈宇轩看到了也加入进来，他提议加一个\"收费亭\"。两个人合作把停车场越搭越大，最后还用积木搭了一个小加油站。整个活动持续了约40分钟，展现了很好的空间想象力和合作能力。",
                "children_names": ["李浩然", "陈宇轩"],
            },
            # 中一班的记录
            {
                "class_id": class2.id, "teacher_id": teachers[1].id,
                "location": "户外操场", "activity_type": "户外活动",
                "observed_at": today - timedelta(days=1),
                "content": "黄梓豪今天在户外拍球，他能连续拍15个，比上周多了5个。吴思颖在旁边跳绳，她正在学习双脚跳，虽然还不太熟练但很努力。郑博文在沙池里挖了一条\"河\"，还用小石头在上面搭了\"桥\"。林可馨和杨子涵一起玩\"过家家\"，林可馨当妈妈，杨子涵当宝宝，两个人玩得很开心。李老师观察发现中一班的孩子们户外活动参与度比上周提高了不少。",
                "children_names": ["黄梓豪", "吴思颖", "郑博文", "林可馨", "杨子涵"],
            },
            {
                "class_id": class2.id, "teacher_id": teachers[2].id,
                "location": "阅读区", "activity_type": "区域活动",
                "observed_at": today - timedelta(days=3),
                "content": "郑博文今天选了一本《好饿的毛毛虫》让陈老师讲给他听。听完之后他指着书上的水果说：\"毛毛虫吃了好多东西呀！\"吴思颖在旁边说：\"它最后变成了蝴蝶！\"郑博文说：\"我也想变成蝴蝶飞来飞去。\"林可馨正在看一本关于颜色的书，她能认出红色、黄色、蓝色等基本颜色。杨子涵在角落里安静地翻看一本汽车画册，陈老师走过去问他在看什么，他指着书上的消防车说：\"这是消防车，能灭火的。\"",
                "children_names": ["郑博文", "吴思颖", "林可馨", "杨子涵"],
            },
            {
                "class_id": class2.id, "teacher_id": teachers[1].id,
                "location": "集体教学", "activity_type": "集体教学",
                "observed_at": today - timedelta(days=5),
                "content": "李老师组织了音乐活动\"小星星\"。林可馨唱歌的声音最大最清楚，她还主动要求领唱。黄梓豪虽然不太爱唱歌，但跟着节奏拍手很认真。杨子涵和吴思颖一起做了星星的手指操，配合得很好。郑博文在活动中间有点走神，李老师走到他身边轻轻拍了拍他的肩膀，他马上又专注了。活动结束后，林可馨说：\"李老师，我们明天还能唱歌吗？\"",
                "children_names": ["林可馨", "黄梓豪", "杨子涵", "吴思颖", "郑博文"],
            },
        ]

        for data in anecdotes_data:
            anecdote = Anecdote(
                class_id=data["class_id"],
                teacher_id=data["teacher_id"],
                location=data["location"],
                activity_type=data["activity_type"],
                observed_at=data["observed_at"],
                content=data["content"],
                status="confirmed",
                recognized_names=",".join(data["children_names"]),
            )
            db.session.add(anecdote)
            db.session.flush()  # 获取anecdote.id

            # 关联幼儿
            for name in data["children_names"]:
                # 在对应班级中查找幼儿
                if data["class_id"] == class1.id:
                    children_list = children_c1
                else:
                    children_list = children_c2

                child = next((c for c in children_list if c.name == name), None)
                if child:
                    ac = AnecdoteChild(
                        anecdote_id=anecdote.id,
                        child_id=child.id,
                        confidence=1.0,
                    )
                    db.session.add(ac)

        db.session.commit()
        print(f"  共创建 {len(anecdotes_data)} 条轶事记录")

        # ===== 5. 创建一个阶段性评估任务（已完成状态，带报告） =====
        print("创建阶段性评估...")

        assessment = Assessment(
            class_id=class1.id,
            title="大一班 2026年4月月度评估",
            period_start=(today - timedelta(days=30)).strftime("%Y-%m-%d"),
            period_end=today.strftime("%Y-%m-%d"),
            status="completed",
            created_by="王老师",
            completed_at=today,
        )
        db.session.add(assessment)
        db.session.flush()

        # 为每位幼儿创建个人报告
        individual_reports = {
            "张梓萱": {
                "content": """## 一、总体评价\n张梓萱本月发展状况良好，在艺术领域表现尤为突出，社会性发展也有明显进步。\n\n## 二、各领域发展分析\n\n### 1. 健康领域\n**发展表现：** 户外活动中参与积极，拍球能连续拍10个以上。午餐时能独立进餐，会主动帮忙分发餐具。\n**发展水平：** B-良好\n\n### 2. 语言领域\n**发展表现：** 能清晰表达自己的想法和需求，在角色游戏中语言丰富，能和同伴进行持续的对话交流。\n**发展水平：** A-优秀\n\n### 3. 社会领域\n**发展表现：** 能与同伴友好合作，在建构区和美工区都能主动与同伴协商分工。乐于帮助他人。\n**发展水平：** A-优秀\n\n### 4. 科学领域\n**发展表现：** 对自然事物有一定好奇心，喜欢观察植物和小动物。\n**发展水平：** B-良好\n\n### 5. 艺术领域\n**发展表现：** 美工区表现突出，彩泥作品造型生动，色彩搭配和谐。喜欢画画，作品富有想象力。\n**发展水平：** A-优秀\n\n## 三、优势与亮点\n- 艺术创造力强，彩泥作品造型生动\n- 社交能力强，善于与同伴合作\n- 语言表达清晰流畅\n\n## 四、关注与建议\n- 科学探究方面可以多引导，鼓励她多去科学区活动\n- 可以提供更多开放性材料激发探索兴趣""",
                "domain_scores": {"健康": 4, "语言": 5, "社会": 5, "科学": 3, "艺术": 5},
            },
            "李浩然": {
                "content": """## 一、总体评价\n李浩然是一个活泼好动、好奇心强的男孩，在科学和健康领域表现突出，但注意力持续时间有待提升。\n\n## 二、各领域发展分析\n\n### 1. 健康领域\n**发展表现：** 大动作发展优秀，跑跳能力强，户外活动参与积极。精细动作在建构区有很好的锻炼。\n**发展水平：** A-优秀\n\n### 2. 语言领域\n**发展表现：** 能表达基本需求，但描述性语言较少，有时会用动作代替语言。\n**发展水平：** B-良好\n\n### 3. 社会领域\n**发展表现：** 能与同伴合作游戏，在建构区和角色区都能融入集体。有时会因为意见不合产生小摩擦。\n**发展水平：** B-良好\n\n### 4. 科学领域\n**发展表现：** 对建构和科学探究有浓厚兴趣，空间想象力好，能发现简单的规律和模式。\n**发展水平：** A-优秀\n\n### 5. 艺术领域\n**发展表现：** 对美术活动兴趣一般，作品相对简单。\n**发展水平：** C-发展中\n\n## 三、优势与亮点\n- 空间建构能力强，停车场作品展现了很好的规划能力\n- 大动作发展优秀\n- 好奇心强，喜欢探索\n\n## 四、关注与建议\n- 鼓励多参与美工区活动，发展艺术表现力\n- 引导用语言描述自己的作品和想法\n- 游戏中遇到分歧时，引导用语言而非行动解决""",
                "domain_scores": {"健康": 5, "语言": 3, "社会": 3, "科学": 5, "艺术": 2},
            },
            "王子墨": {
                "content": """## 一、总体评价\n王子墨是一个安静内敛的孩子，喜欢阅读和观察，语言和认知发展良好，但社交主动性需要加强。\n\n## 二、各领域发展分析\n\n### 1. 健康领域\n**发展表现：** 喜欢安静的户外活动，大动作发展中等，平衡木走得较稳。\n**发展水平：** B-良好\n\n### 2. 语言领域\n**发展表现：** 词汇量丰富，能用完整的句子表达想法。在阅读区经常能说出让老师惊喜的话。\n**发展水平：** A-优秀\n\n### 3. 社会领域\n**发展表现：** 能与熟悉的同伴交往，但在新环境中较慢热。在刘诗涵的带动下参与度有所提高。\n**发展水平：** C-发展中\n\n### 4. 科学领域\n**发展表现：** 观察能力强，能注意到事物的细节。喜欢阅读科普类绘本。\n**发展水平：** A-优秀\n\n### 5. 艺术领域\n**发展表现：** 对美术活动兴趣一般，作品较少。\n**发展水平：** C-发展中\n\n## 三、优势与亮点\n- 语言表达能力强，词汇丰富\n- 观察细致，能发现事物的细节特征\n- 专注力好，阅读时能持续较长时间\n\n## 四、关注与建议\n- 鼓励参与更多集体活动和户外游戏\n- 创造机会让他与不同同伴互动\n- 引导参与美工和音乐活动""",
                "domain_scores": {"健康": 3, "语言": 5, "社会": 2, "科学": 5, "艺术": 2},
            },
        }

        for child in children_c1:
            if child.name in individual_reports:
                report_data = individual_reports[child.name]
                report = AssessmentReport(
                    assessment_id=assessment.id,
                    report_type="individual",
                    child_id=child.id,
                    content=report_data["content"],
                    domain_scores=str(report_data["domain_scores"]),
                )
                db.session.add(report)

        # 班级汇总报告
        class_summary = AssessmentReport(
            assessment_id=assessment.id,
            report_type="class_summary",
            child_id=None,
            content="""## 一、班级发展概况\n大一班本月整体发展状况良好。8名幼儿在各领域均有不同程度的进步，班级整体氛围积极向上，同伴关系融洽。\n\n## 二、各领域发展状况\n\n### 健康领域\n班级整体大动作发展良好，大部分幼儿能积极参与户外活动。李浩然、陈宇轩表现尤为突出。精细动作方面，建构区和美工区的活动为幼儿提供了充分的锻炼机会。\n\n### 语言领域\n语言发展整体较好。张梓萱、王子墨、刘诗涵语言表达能力较强，能进行连贯的对话交流。李浩然、孙一诺在描述性语言方面还有提升空间。\n\n### 社会领域\n班级社交氛围良好，大部分幼儿能与同伴友好相处。张梓萱、刘诗涵、赵雨桐社交能力突出。王子墨需要更多鼓励来提升社交主动性。\n\n### 科学领域\n陈宇轩、李浩然在科学探究方面表现出浓厚兴趣和较强能力。其他幼儿对科学活动也有一定参与度。\n\n### 艺术领域\n张梓萱、周欣怡在艺术领域表现突出。部分男生对美术活动兴趣不高，需要通过更多元的艺术活动形式来激发兴趣。\n\n## 三、共性特征与优势\n- 班级合作意识强，建构区和角色区经常出现自发的小组合作\n- 语言交流氛围好，孩子们愿意分享和讨论\n- 户外活动参与度本月明显提高\n\n## 四、需关注的问题\n- 王子墨的社交主动性需要持续关注和支持\n- 李浩然在同伴冲突时的情绪管理需要引导\n- 部分幼儿对美工和音乐活动的参与度不高\n\n## 五、班级发展建议\n- 增加更多开放性的艺术活动，吸引不同兴趣的幼儿参与\n- 创造更多混龄或跨组合作的机会\n- 在科学区投放更多探究性材料""",
        )
        db.session.add(class_summary)

        # 教育反思报告
        reflection = AssessmentReport(
            assessment_id=assessment.id,
            report_type="reflection",
            child_id=None,
            content="""## 一、教育实践反思\n本月教育实践整体效果良好。区域活动的材料投放基本满足幼儿需求，但美工区的材料种类可以更加丰富。集体教学活动中，孩子们的参与度较高，但个别活动的设计可以更加游戏化。\n\n## 二、个别化支持策略\n\n### 王子墨\n- 在区域活动时安排性格开朗的同伴与其合作\n- 鼓励他在集体面前分享自己的阅读发现\n- 逐步扩大他的社交圈\n\n### 李浩然\n- 在建构区提供更多挑战性的搭建任务\n- 引导他用语言而非行动表达想法\n- 情绪管理方面进行正向强化\n\n## 三、环境与材料调整建议\n- 美工区增加自然材料（树叶、石头、树枝等）\n- 科学区投放放大镜、磁铁等探究工具\n- 阅读区补充更多科普类和非虚构类绘本\n\n## 四、家园共育建议\n- 建议家长每天与孩子进行15分钟以上的亲子阅读\n- 鼓励家长周末带孩子进行户外探索活动\n- 关注孩子的情绪变化，及时与老师沟通\n\n## 五、下阶段观察重点\n- 王子墨的社交参与度变化\n- 李浩然的情绪管理和同伴冲突解决方式\n- 幼儿在艺术活动中的参与和表现\n- 班级合作游戏的深度和持续性""",
        )
        db.session.add(reflection)

        db.session.commit()
        print(f"  创建评估任务: {assessment.title}")
        print(f"  个人报告: {len(individual_reports)}份")
        print("  班级汇总报告: 1份")
        print("  教育反思报告: 1份")

        # ===== 统计 =====
        print("\n===== 测试数据创建完成 =====")
        print(f"班级: 2个")
        print(f"幼儿: {len(children_c1) + len(children_c2)}名")
        print(f"教师: {len(teachers)}名")
        print(f"轶事记录: {len(anecdotes_data)}条")
        print(f"评估任务: 1个（含{len(individual_reports)+2}份报告）")


if __name__ == "__main__":
    seed()

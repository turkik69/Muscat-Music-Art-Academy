"""Generate the academy's Arabic and English static website."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BASE = "https://muscat-music-art-academy-2026.turki-k69.chatgpt.site"

SOURCES = {
    "museum": "https://www.nm.gov.om/en/news/the-national-museum-signs-a-cooperation-programme-with-the-muscat-music-and-art-academy",
    "summer": "https://www.nm.gov.om/en/news/the-national-museum-hosts-the-closing-ceremony-of-the-muscat-academy-of-music-and-arts-summer-program",
    "ministry": "https://www.mcsy.gov.om/news/the-ministry-of-culture-sports-and-youth-launches-music-courses-in-partnership-with-the-muscat-academy-of-music-and-arts",
    "trinity": "https://www.trinitycollege.com/local-trinity/oman",
    "award": "https://www.londonarabia.com/winners-2018",
    "education": "https://alroya.om/post/227801/%D9%85%D9%86%D8%AD-%D8%AF-%D8%B4%D8%B1%D9%8A%D9%81%D8%A9-%D8%A7%D9%84%D9%8A%D8%AD%D9%8A%D8%A7%D8%A6%D9%8A%D8%A9-%D8%AC%D8%A7%D8%A6%D8%B2%D8%A9-%D8%A7%D9%84%D9%85%D8%B1%D8%A3%D8%A9-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-%D9%84%D9%84%D8%B9%D8%A7%D9%85-2018",
    "graduates": "https://alroya.om/post/385441/%D8%A7%D9%84%D8%B4%D9%8A%D8%A8%D8%A7%D9%86%D9%8A%D8%A9-%D8%AA%D8%B1%D8%B9%D9%89-%D8%AA%D8%AE%D8%B1%D9%8A%D8%AC-%D8%A7%D9%84%D9%81%D9%88%D8%AC-%D8%A7%D9%84%D8%A3%D9%88%D9%84-%D9%85%D9%86-%D8%AD%D9%85%D9%84%D8%A9-%D8%B4%D9%87%D8%A7%D8%AF%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%B1%D8%A7%D8%AD%D9%84-%D8%A7%D9%84%D8%B3%D8%A7%D8%AF%D8%B3%D8%A9-%D9%88%D8%A7%D9%84%D8%AB%D8%A7%D9%85%D9%86%D8%A9-%D9%81%D9%8A-%D8%A7%D9%84%D8%A3%D8%AF%D8%A7%D8%A1-%D8%A7%D9%84%D9%85%D9%88%D8%B3%D9%8A%D9%82%D9%8A",
}

NAV = {
    "ar": [("index", "الرئيسية"), ("about", "عن الأكاديمية"), ("programs", "البرامج"), ("admissions", "الالتحاق"), ("news", "الأخبار"), ("contact", "تواصل معنا")],
    "en": [("index", "Home"), ("about", "About"), ("programs", "Programmes"), ("admissions", "Admissions"), ("news", "News"), ("contact", "Contact")],
}

TEXT = {
    "ar": {
        "brand": "أكاديمية مسقط للموسيقى والفنون", "tag": "MUSCAT MUSIC & ART ACADEMY", "apply": "استفسر عن الالتحاق", "skip": "انتقل إلى المحتوى",
        "footer": "حيث يلتقي التعليم بالموسيقى والفنون في مسقط.", "location": "شاطئ القرم، مسقط، سلطنة عُمان", "privacy": "الخصوصية", "back": "العودة للأعلى",
        "illustrative": "صورة توضيحية وليست لمقر الأكاديمية", "read": "اقرأ الخبر", "source": "المصدر الرسمي", "learn": "اعرف المزيد", "all": "عرض جميع البرامج",
    },
    "en": {
        "brand": "Muscat Music & Art Academy", "tag": "أكاديمية مسقط للموسيقى والفنون", "apply": "Enquire about joining", "skip": "Skip to content",
        "footer": "Where learning meets music and art in Muscat.", "location": "Shatti Al Qurum, Muscat, Oman", "privacy": "Privacy", "back": "Back to top",
        "illustrative": "Illustrative image; not the academy premises", "read": "Read story", "source": "Official source", "learn": "Learn more", "all": "Explore all programmes",
    },
}

def path(page, lang):
    name = "index.html" if page == "index" else f"{page}.html"
    return ("en/" if lang == "en" else "") + name

def link(page, lang, label=None, cls=""):
    label = label or dict(NAV[lang]).get(page, page)
    return f'<a class="{cls}" href="/{path(page,lang)}">{label}</a>'

def external(url, label, cls=""):
    return f'<a class="{cls}" href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true"> ↗</span></a>'

def source_link(key, label, cls=""):
    return external(SOURCES[key], label, cls)

def page_head(page, lang, title, description):
    t = TEXT[lang]
    other = "en" if lang == "ar" else "ar"
    asset = "assets"
    nav = "".join(link(key, lang, label, 'active' if key == page else '') for key, label in NAV[lang])
    return f'''<!doctype html><html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#17211f"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="أكاديمية مسقط">
<meta name="description" content="{escape(description,quote=True)}"><title>{escape(title)} | {t['brand']}</title>
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)} | {escape(t['brand'],quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:image" content="{BASE}/assets/academy-emblem.webp">
<link rel="icon" type="image/png" sizes="32x32" href="/{asset}/favicon-32.png"><link rel="apple-touch-icon" sizes="180x180" href="/{asset}/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest"><link rel="stylesheet" href="/styles.css?v=20261119c">
<link rel="alternate" hreflang="ar" href="{BASE}/{path(page,'ar')}"><link rel="alternate" hreflang="en" href="{BASE}/{path(page,'en')}">
<script defer src="/site.js"></script></head><body>
<a class="skip" href="#main">{t['skip']}</a><div class="utility"><div class="container"><span>{t['location']}</span><a href="mailto:info@muscatmusicartacademy.com">info@muscatmusicartacademy.com</a></div></div>
<header class="site-header" id="top"><div class="container header-row">
<a class="identity" href="/{path('index',lang)}" aria-label="{t['brand']}"><img src="/assets/academy-emblem.webp" alt=""><span><strong>{t['brand']}</strong><small>{t['tag']}</small></span></a>
<button class="menu-button" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="{'القائمة' if lang=='ar' else 'Menu'}"><span></span><span></span><span></span></button>
<nav class="site-nav" id="site-nav" aria-label="{'القائمة الرئيسية' if lang=='ar' else 'Main navigation'}">{nav}</nav>
<div class="header-tools"><a class="language" href="/{path(page,other)}" lang="{other}" hreflang="{other}">{'English' if lang=='ar' else 'العربية'}</a>{link('admissions',lang,t['apply'],'header-cta')}</div>
</div></header><main id="main">'''

def page_foot(lang):
    t=TEXT[lang]
    nav="".join(link(key,lang,label) for key,label in NAV[lang])
    return f'''</main><footer class="site-footer"><div class="container footer-grid"><div class="footer-identity"><img src="/assets/academy-emblem.webp" alt=""><strong>{t['brand']}</strong><p>{t['footer']}</p></div><div><span class="footer-label">{'تصفح' if lang=='ar' else 'Explore'}</span><nav>{nav}</nav></div><div><span class="footer-label">{'تواصل' if lang=='ar' else 'Connect'}</span><p>{t['location']}</p><a href="tel:+96871498887" dir="ltr">+968 7149 8887</a><a href="mailto:info@muscatmusicartacademy.com">info@muscatmusicartacademy.com</a>{external('https://www.instagram.com/muscatmaa/','Instagram @muscatmaa')}</div></div><div class="container footer-base"><span>© <span data-year></span> Muscat Music & Art Academy</span><div>{link('privacy',lang,t['privacy'])}<a href="#top">{t['back']} ↑</a></div></div></footer></body></html>'''

def section_intro(kicker, title, summary=""):
    return f'<div class="section-intro"><span class="eyebrow">{kicker}</span><h2>{title}</h2>{f"<p>{summary}</p>" if summary else ""}</div>'

def founder_feature(lang, compact=False):
    if lang=='ar':
        kicker='المؤسس والرئيس التنفيذي'; name='<span class="founder-honorific">معالي الدكتورة</span> <span class="founder-full-name">شريفة بنت خلفان بن ناصر اليحيائية</span>'; role='وزيرة التنمية الاجتماعية سابقًا · أكاديمية وباحثة عُمانية'
        bio='تقود الدكتورة شريفة أكاديمية مسقط للموسيقى والفنون منذ تأسيسها عام 2019. تمتد مسيرتها بين التعليم والبحث والعمل الوطني، وتضع تنمية المواهب الفنية في صميم رحلة الأكاديمية.'
        cta='اقرأ سيرة المؤسس'; alt='صورة شخصية للدكتورة شريفة اليحيائية'
    else:
        kicker='FOUNDER & CHIEF EXECUTIVE OFFICER'; name='H.E. Dr Sharifa bint Khalfan bin Nasser Al Yahyai'; role='Former Minister of Social Development · Omani academic and researcher'
        bio='Dr Sharifa has led Muscat Music & Art Academy since its founding in 2019. Her career spans education, research and national service, with a focus on creating opportunities for emerging artistic talent.'
        cta='Meet the founder'; alt='Portrait of Dr Sharifa Al Yahyai'
    return f'''<div class="founder-feature {'compact' if compact else ''}"><div class="founder-image"><div class="portrait-photo"><img src="/assets/founder-cutout.webp" alt="{alt}" loading="lazy" width="1314" height="1197"></div></div><div class="founder-text"><span class="eyebrow">{kicker}</span><h2>{name}</h2><p class="founder-role">{role}</p><p>{bio}</p>{link('about',lang,cta,'text-arrow') if compact else ''}</div></div>'''

def home(lang):
    t=TEXT[lang]
    if lang=='ar':
        hero_k='منذ عام 2019 · مسقط، سلطنة عُمان'; hero_t='الفن يبدأ<br>من <em>هنا.</em>'; hero_p='موسيقى، فنون بصرية، وحركة. مساحة يتعلّم فيها الأطفال والكبار، يكتشفون مواهبهم، ويطورونها بالممارسة.'
        pillars=[('01','الموسيقى','من العزف والغناء إلى النظريات الموسيقية، بخيارات تعليم تناسب مستويات مختلفة.'),('02','الفنون البصرية','الرسم والتلوين وتجارب فنية تفتح مجالًا للتعبير والخيال.'),('03','الباليه والحركة','تنمية الإيقاع والتوازن والتعبير الحركي في بيئة تعليمية مشجعة.')]
        about_k='عن الأكاديمية'; about_t='تعليم فني يفتح <em>آفاقًا جديدة.</em>'; about_p='تأسست أكاديمية مسقط للموسيقى والفنون عام 2019 في سلطنة عُمان. تجمع برامجها بين التعليم المنظم والتجربة الفنية، وتستقبل الراغبين في التعلم من الأطفال والبالغين.'
        proof_k='من مسيرتنا'; proof_t='شراكات تعزز <em>التعلّم والمشاركة.</em>'; stories=[('2025','برنامج تعاون مع المتحف الوطني','لتوسيع التدريب والمشاركة الفنية والثقافية.','museum'),('2026','دورات موسيقية بالشراكة مع الوزارة','برنامج تدريب شمل البيانو والجيتار والغناء الجماعي.','ministry')]
        news_k='أخبار الأكاديمية'; news_t='من قاعات التعلم إلى <em>المشهد الثقافي.</em>'; final_t='كل رحلة فنية تبدأ بخطوة.'; final_p='أخبرنا بالمجال الذي يهمك، وسنساعدك في معرفة الخيارات المتاحة.'
    else:
        hero_k='SINCE 2019 · MUSCAT, OMAN'; hero_t='Art starts<br><em>here.</em>'; hero_p='Music, visual arts and movement. A place for children and adults to discover, practise and develop their creative abilities.'
        pillars=[('01','Music','From instruments and singing to music theory, with learning options for different levels.'),('02','Visual arts','Drawing, painting and creative practice that make room for expression.'),('03','Ballet & movement','Develop rhythm, balance and movement in an encouraging learning environment.')]
        about_k='ABOUT THE ACADEMY'; about_t='Arts education with <em>room to grow.</em>'; about_p='Founded in 2019 in Oman, Muscat Music & Art Academy combines structured learning with artistic exploration for children and adults.'
        proof_k='OUR STORY'; proof_t='Partnerships that support <em>learning and participation.</em>'; stories=[('2025','National Museum cooperation','Expanding cultural and artistic training and participation.','museum'),('2026','Music courses with the ministry','A training programme covering piano, guitar and group singing.','ministry')]
        news_k='ACADEMY NEWS'; news_t='From learning rooms to <em>the cultural stage.</em>'; final_t='Every creative journey starts somewhere.'; final_p='Tell us what you are interested in and we will help you explore the available options.'
    cards=''.join(f'<article class="pillar"><span>{n}</span><h3>{h}</h3><p>{p}</p></article>' for n,h,p in pillars)
    stories_html=''.join(f'<article class="story"><span class="story-date">{yr}</span><h3>{title}</h3><p>{desc}</p>{source_link(key,t["source"])}</article>' for yr,title,desc,key in stories)
    return f'''<section class="hero"><div class="container hero-inner"><div class="hero-copy"><span class="eyebrow">{hero_k}</span><h1>{hero_t}</h1><p>{hero_p}</p><div class="hero-actions">{link('programs',lang,t['all'],'btn btn-gold')}{link('admissions',lang,t['apply'],'underlined')}</div><div class="hero-index">MUSIC <span>✦</span> ART <span>✦</span> MOVEMENT</div></div><div class="hero-image"><img src="/assets/visual-2.webp" alt="{'آلات موسيقية في مشهد توضيحي' if lang=='ar' else 'Illustrative still life of musical instruments'}"><small>{t['illustrative']}</small></div></div></section>
<section class="pillars-section"><div class="container pillars">{cards}</div></section>
<section class="section about-teaser"><div class="container split-intro">{section_intro(about_k,about_t,about_p)}<div class="about-visual"><img src="/assets/visual-3.webp" loading="lazy" alt="{'مساحة فنية توضيحية' if lang=='ar' else 'Illustrative visual arts studio'}"><small>{t['illustrative']}</small></div></div></section>
<section class="section founder-home"><div class="container">{founder_feature(lang,True)}</div></section>
<section class="section proof"><div class="container">{section_intro(proof_k,proof_t)}<div class="story-grid">{stories_html}</div></div></section>
<section class="section news-teaser"><div class="container news-teaser-row"><div>{section_intro(news_k,news_t)}</div>{link('news',lang,t['learn'],'text-arrow')}</div></section>
<section class="bottom-cta"><div class="container"><h2>{final_t}</h2><p>{final_p}</p>{link('admissions',lang,t['apply'],'btn btn-gold')}</div></section>'''

def about(lang):
    if lang=='ar':
        heading='عن أكاديمية مسقط للموسيقى والفنون'; sub='مساحة تجمع التعليم الفني، الممارسة، وفرص المشاركة الثقافية في مسقط.'
        intro='منذ تأسيسها عام 2019، تعمل الأكاديمية على تقديم تعليم الموسيقى والفنون والحركة للأطفال والكبار، وتربط التعلم بالممارسة والظهور الفني.'
        vision='أن يجد كل متعلم مدخلًا مناسبًا للفن، ومساحة يطور فيها قدراته وثقته ويشارك أثره مع المجتمع.'
        mission='تقديم مسارات تعليمية فنية منظمة تشجع على التجربة والتدريب المستمر، وتفتح أبواب التواصل مع المؤسسات الثقافية والتعليمية.'
        founder_title='من التعليم والخدمة العامة إلى تأسيس الأكاديمية'; degree='المؤهلات الأكاديمية'; mile='محطات المسيرة'; message='رسالة المؤسس'; message_body='تسعى الأكاديمية إلى إتاحة فرصة حقيقية لاكتشاف الموهبة وصقلها، وأن يكون تعليم الفن جزءًا من بناء الإنسان وحضوره في المجتمع.'
        note='هذه صياغة تعريفية مستندة إلى أنشطة الأكاديمية، وليست اقتباسًا مباشرًا من المؤسس.'
        degrees=[('1992','بكالوريوس اللغة العربية وآدابها، جامعة السلطان قابوس'),('1995','ماجستير الأدب الحديث، جامعة السلطان قابوس'),('2001','دكتوراه دراسات اللغة العربية والشرق الأوسط، جامعة ليدز')]
        milestones=[('2004–2011','وزيرة التنمية الاجتماعية في سلطنة عُمان'),('2018','جائزة المرأة العربية عن الإنجاز في التنمية الاجتماعية'),('2019','تأسيس أكاديمية مسقط للموسيقى والفنون'),('2025','توقيع برنامج تعاون مع المتحف الوطني')]
        sources='مصادر السيرة والمعلومات'; slogan='رؤيتنا'; mlabel='رسالتنا'
    else:
        heading='About Muscat Music & Art Academy'; sub='A place in Muscat where arts education, practice and cultural participation meet.'
        intro='Since its founding in 2019, the academy has offered music, visual arts and movement learning for children and adults, connecting lessons with practice and artistic participation.'
        vision='To give every learner a welcoming entry to the arts and room to build skills, confidence and a connection with the community.'
        mission='To offer structured arts learning that encourages exploration, regular practice and connections with cultural and educational institutions.'
        founder_title='From education and public service to the academy'; degree='Academic background'; mile='Career milestones'; message='A message from the founder'; message_body='The academy seeks to give people a real opportunity to discover and develop their talents, making arts education part of personal growth and community life.'
        note='Editorial summary based on the academy’s activities; not a direct quotation from the founder.'
        degrees=[('1992','BA in Arabic Language and Literature, Sultan Qaboos University'),('1995','MA in Modern Literature, Sultan Qaboos University'),('2001','PhD in Arabic and Middle Eastern Studies, University of Leeds')]
        milestones=[('2004–2011','Minister of Social Development, Sultanate of Oman'),('2018','Arab Woman of the Year Award for social development'),('2019','Founded Muscat Music & Art Academy'),('2025','Signed a cooperation programme with the National Museum')]
        sources='Sources and further reading'; slogan='Our vision'; mlabel='Our mission'
    def timeline(rows): return ''.join(f'<li><strong>{year}</strong><span>{value}</span></li>' for year,value in rows)
    return f'''<section class="page-banner"><div class="container"><span class="eyebrow">{'OUR STORY' if lang=='en' else 'قصتنا'}</span><h1>{heading}</h1><p>{sub}</p></div></section>
<section class="section"><div class="container about-opening"><p class="large-copy">{intro}</p><div class="principles"><div><span>01</span><h2>{slogan}</h2><p>{vision}</p></div><div><span>02</span><h2>{mlabel}</h2><p>{mission}</p></div></div></div></section>
<section class="section founder-page"><div class="container"><div class="founder-page-head">{section_intro('FOUNDER / المؤسس',founder_title)}</div>{founder_feature(lang)}</div></section>
<section class="section biography"><div class="container bio-grid"><div><span class="eyebrow">{degree}</span><ol class="timeline">{timeline(degrees)}</ol></div><div><span class="eyebrow">{mile}</span><ol class="timeline">{timeline(milestones)}</ol></div></div><div class="container founder-quote"><span class="eyebrow">{message}</span><p>{message_body}</p><small>{note}</small></div><div class="container sources"><strong>{sources}</strong>{source_link('museum','National Museum')}{source_link('award','Arab Women Awards')}{source_link('education','Education & career')}</div></section>'''

def programs(lang):
    if lang=='ar':
        title='برامج الموسيقى والفنون'; subtitle='مجالات متعددة، ونقطة بداية تناسب اهتمامك ومستواك.'; intro='تعرّف على المجالات التعليمية الرئيسية. تواصل مع فريق الأكاديمية لمعرفة البرامج المتاحة حاليًا، الأعمار المناسبة، المواعيد، والرسوم.'
        items=[('الموسيقى والآلات','البيانو، الكمان، التشيلو، الغيتار، العود، القانون، وآلات الإيقاع والنفخ.','يمكن اختيار مسار فردي أو جماعي حسب البرنامج المتاح.','visual-2.webp'),('الغناء والنظريات الموسيقية','الغناء، الصولفيج، ومبادئ القراءة والتذوق الموسيقي.','لمن يرغب في بناء أساس معرفي وأدائي متدرج.','visual-1.webp'),('الفنون البصرية','الرسم والتلوين بالفحم والرصاص والألوان المائية والأكريليك وغيرها.','مساحة لممارسة التقنيات والتعبير الفني.','visual-3.webp'),('الباليه والحركة','الباليه والجمباز الإيقاعي والتعبير الحركي.','تختلف الفئات العمرية وشروط المشاركة بحسب البرنامج.','visual-3.webp')]
        pathway='مسارات التقييم الموسيقي'; path_text='ترد الأكاديمية في قائمة مراكز Trinity College London في عُمان. وقد نشرت الصحافة العُمانية خبر برنامج شهادات المدارس الملكية البريطانية للموسيقى (ABRSM) وتخريج الفوج الأول من المراحل السادسة والثامنة في 2026. اسأل الأكاديمية عن شروط الاختبارات والاعتمادات السارية لكل مسار.'
        source='تحقق من المصادر'; footer='هل عرفت المجال الذي يهمك؟'; footerp='ارسل استفسارًا موجزًا لتحصل على معلومات البرامج والمواعيد.'
    else:
        title='Music and arts programmes'; subtitle='Different disciplines, with a starting point for your interests and level.'; intro='Explore the academy’s main areas of learning. Contact the team for current availability, age requirements, schedules and fees.'
        items=[('Music & instruments','Piano, violin, cello, guitar, oud, qanun, percussion and wind instruments.','Individual or group learning options vary by available programme.','visual-2.webp'),('Singing & music theory','Voice, solfeggio and the foundations of reading and understanding music.','Build a gradual foundation in knowledge and performance.','visual-1.webp'),('Visual arts','Drawing and painting with pencil, charcoal, watercolour, acrylic and more.','Explore techniques and personal expression.','visual-3.webp'),('Ballet & movement','Ballet, rhythmic gymnastics and expressive movement.','Age groups and participation requirements vary by programme.','visual-3.webp')]
        pathway='Music examination pathways'; path_text='The academy appears on Trinity College London’s list of centres in Oman. Omani press has also reported an ABRSM programme and the first cohort of Grade 6 and 8 music performance graduates in 2026. Ask the academy which examinations and accreditations currently apply to each pathway.'
        source='Explore sources'; footer='Found a discipline that interests you?'; footerp='Send a short enquiry to find out about programmes and schedules.'
    cards=''.join(f'<article class="discipline"><div class="discipline-img"><img src="/assets/{img}" loading="lazy" alt="{'صورة توضيحية' if lang=='ar' else 'Illustrative image'}"><small>{TEXT[lang]["illustrative"]}</small></div><div><span class="eyebrow">{str(i+1).zfill(2)} / 04</span><h2>{name}</h2><p>{desc}</p><small>{note}</small>{link("admissions",lang,TEXT[lang]["apply"],"text-arrow")}</div></article>' for i,(name,desc,note,img) in enumerate(items))
    return f'''<section class="page-banner"><div class="container"><span class="eyebrow">{'LEARNING PATHWAYS' if lang=='en' else 'مسارات التعلم'}</span><h1>{title}</h1><p>{subtitle}</p></div></section><section class="section"><div class="container"><p class="large-copy program-intro">{intro}</p><div class="disciplines">{cards}</div></div></section><section class="section pathway"><div class="container pathway-grid"><div><span class="eyebrow">TRINITY · ABRSM</span><h2>{pathway}</h2></div><div><p>{path_text}</p><div class="source-buttons">{source_link('trinity','Trinity College London')}{source_link('graduates','ABRSM 2026')}</div></div></div></section><section class="bottom-cta"><div class="container"><h2>{footer}</h2><p>{footerp}</p>{link('admissions',lang,TEXT[lang]['apply'],'btn btn-gold')}</div></section>'''

def admissions(lang):
    if lang=='ar':
        title='الالتحاق بالأكاديمية'; subtitle='ابدأ باستفسار بسيط، ثم تعرّف على المسار الذي يناسبك.'
        steps=[('01','اختر المجال','تصفح الموسيقى والفنون البصرية والباليه والحركة.'),('02','أرسل استفسارك','اذكر الفئة العمرية والمجال الذي ترغب في دراسته.'),('03','ناقش التفاصيل','يساعدك فريق الأكاديمية في معرفة المواعيد والرسوم والمستوى المناسب قبل تأكيد الالتحاق.')]
        formtitle='أخبرنا بما تريد تعلمه'; formsub='سنجهز رسالة واتساب لتراجعها وترسلها إلى الأكاديمية بنفسك.'; name='الاسم'; age='الفئة العمرية'; interest='المجال'; note='ملاحظات أو أسئلة (اختياري)'; choose='اختر'; child='طفل'; teen='ناشئ'; adult='بالغ'; options=['الموسيقى','الفنون البصرية','الباليه والحركة']; submit='متابعة عبر واتساب'; privacy='لا يحتفظ هذا الموقع بمعلومات الاستفسار. لن تُرسل الرسالة إلا بعد موافقتك داخل واتساب.'
        faq='أسئلة متكررة'; faqs=[('هل توجد برامج للأطفال والكبار؟','نعم، لكن الفئات العمرية تختلف بحسب البرنامج. تواصل مع الأكاديمية لتأكيد المتاح.'),('هل تظهر الرسوم والمواعيد هنا؟','تتغير بحسب البرنامج والفصل؛ يزوّدك فريق الأكاديمية بالتفاصيل الحالية.'),('هل يُعد إرسال الاستفسار تسجيلًا نهائيًا؟','لا. الاستفسار يفتح باب التواصل، ويُؤكد الالتحاق بعد مراجعة تفاصيل البرنامج مع الأكاديمية.')]
    else:
        title='Joining the academy'; subtitle='Start with a simple enquiry, then discover the path that fits you.'
        steps=[('01','Choose an area','Explore music, visual arts, ballet and movement.'),('02','Send an enquiry','Tell us the learner’s age group and area of interest.'),('03','Discuss the details','The academy team can explain current schedules, fees and levels before enrolment is confirmed.')]
        formtitle='Tell us what you would like to learn'; formsub='We will prepare a WhatsApp message for you to review and send to the academy.'; name='Name'; age='Age group'; interest='Area of interest'; note='Questions or notes (optional)'; choose='Choose'; child='Child'; teen='Teen'; adult='Adult'; options=['Music','Visual arts','Ballet & movement']; submit='Continue on WhatsApp'; privacy='This website does not retain your enquiry. Nothing is sent until you approve it in WhatsApp.'
        faq='Frequently asked questions'; faqs=[('Are there programmes for children and adults?','Yes. Age requirements vary by programme; ask the academy about current options.'),('Are fees and schedules listed here?','They can change by programme and term. The academy team will provide current details.'),('Is an enquiry a confirmed enrolment?','No. It begins a conversation; enrolment is confirmed after discussing the programme with the academy.')]
    steps_html=''.join(f'<div class="admission-step"><span>{n}</span><h3>{h}</h3><p>{p}</p></div>' for n,h,p in steps)
    faq_html=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
    return f'''<section class="page-banner"><div class="container"><span class="eyebrow">{'ADMISSIONS' if lang=='en' else 'رحلة الالتحاق'}</span><h1>{title}</h1><p>{subtitle}</p></div></section><section class="section"><div class="container admission-steps">{steps_html}</div></section>
<section class="section enquiry-section" id="enquiry"><div class="container enquiry-grid"><div>{section_intro('START HERE / ابدأ هنا',formtitle,formsub)}<p class="form-privacy">{privacy}</p></div><form id="enquiry-form" data-lang="{lang}"><label for="full-name">{name}</label><input id="full-name" name="name" autocomplete="name" maxlength="80" required><label for="interest">{interest}</label><select id="interest" name="interest" required><option value="">{choose}</option>{''.join(f'<option value="{key}">{label}</option>' for key,label in zip(['music','arts','movement'],options))}</select><label for="age">{age}</label><select id="age" name="age" required><option value="">{choose}</option><option value="child">{child}</option><option value="teen">{teen}</option><option value="adult">{adult}</option></select><label for="note">{note}</label><textarea id="note" name="note" rows="4" maxlength="500"></textarea><button class="btn btn-gold" type="submit">{submit}<span aria-hidden="true">↗</span></button></form></div></section><section class="section faq"><div class="container"><h2>{faq}</h2><div>{faq_html}</div></div></section>'''

def news(lang):
    if lang=='ar':
        title='أخبار وشراكات الأكاديمية'; subtitle='محطات موثقة من عمل الأكاديمية ومشاركاتها.'
        cards=[('2026','برنامج دورات موسيقية بالشراكة مع وزارة الثقافة والرياضة والشباب','أعلنت الوزارة برامج تدريبية في البيانو والجيتار والغناء الجماعي ضمن أجندة 2026.','ministry'),('2025','برنامج تعاون مع المتحف الوطني','وقعت الدكتورة شريفة اليحيائية باسم الأكاديمية برنامج تعاون في الثقافة والموسيقى والتعليم والتدريب.','museum'),('2025','ختام البرنامج الصيفي في المتحف الوطني','استضاف المتحف الوطني ختام برنامج أكاديمية مسقط الصيفي بمشاركة 32 متدربًا.','summer'),('2026','تخريج الفوج الأول من المراحل الموسيقية المتقدمة','تناولت الصحافة العُمانية تخريج حملة شهادات المرحلتين السادسة والثامنة في الأداء الموسيقي ضمن برنامج ABRSM.','graduates')]
    else:
        title='Academy news & partnerships'; subtitle='Documented milestones in the academy’s work and participation.'
        cards=[('2026','Music courses with the Ministry of Culture, Sports and Youth','The ministry announced piano, guitar and group singing courses in its 2026 programme.','ministry'),('2025','National Museum cooperation programme','Dr Sharifa signed an agreement on behalf of the academy covering culture, music, education and training.','museum'),('2025','Summer programme concludes at the National Museum','The museum hosted the academy’s summer programme closing event with 32 participants.','summer'),('2026','First cohort of advanced music grades','Omani press reported the graduation of Grade 6 and 8 music performance students in an ABRSM programme.','graduates')]
    html=''.join(f'<article class="news-card"><span class="news-year">{year}</span><h2>{h}</h2><p>{p}</p>{source_link(k,TEXT[lang]["read"],"text-arrow")}</article>' for year,h,p,k in cards)
    return f'''<section class="page-banner"><div class="container"><span class="eyebrow">{'NEWS & COLLABORATIONS' if lang=='en' else 'الأخبار والتعاون'}</span><h1>{title}</h1><p>{subtitle}</p></div></section><section class="section"><div class="container news-grid">{html}</div></section>'''

def contact(lang):
    if lang=='ar':
        title='تواصل مع الأكاديمية'; subtitle='نرحب باستفساراتك حول البرامج والمواعيد والالتحاق.'; place='المقر'; tel='الهاتف وواتساب'; mail='البريد الإلكتروني'; social='إنستغرام'; hello='لنبدأ الحديث'; prompt='اختر وسيلة التواصل الأنسب لك، أو أرسل استفسارًا عن الالتحاق.'
    else:
        title='Contact the academy'; subtitle='We welcome your questions about programmes, schedules and enrolment.'; place='Location'; tel='Phone & WhatsApp'; mail='Email'; social='Instagram'; hello='Let’s talk'; prompt='Choose the contact option that suits you, or send an admissions enquiry.'
    return f'''<section class="page-banner"><div class="container"><span class="eyebrow">CONTACT / تواصل</span><h1>{title}</h1><p>{subtitle}</p></div></section><section class="section"><div class="container contact-layout"><div class="contact-intro"><h2>{hello}</h2><p>{prompt}</p>{link('admissions',lang,TEXT[lang]['apply'],'btn btn-gold')}</div><div class="contact-info"><div><span>{place}</span><strong>{TEXT[lang]['location']}</strong></div><div><span>{tel}</span><a dir="ltr" href="tel:+96871498887">+968 7149 8887</a><a href="https://wa.me/96871498887" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a></div><div><span>{mail}</span><a href="mailto:info@muscatmusicartacademy.com">info@muscatmusicartacademy.com</a></div><div><span>{social}</span>{external('https://www.instagram.com/muscatmaa/','@muscatmaa')}</div></div></div></section>'''

def privacy(lang):
    if lang=='ar':
        title='الخصوصية'; intro='هذا الموقع التعريفي لا ينشئ حسابات مستخدمين ولا يخزن بيانات استفسارات الالتحاق على خادمه.'
        body='<h2>استفسارات الالتحاق</h2><p>عند تعبئة نموذج الاستفسار، يُنشئ متصفحك رسالة جاهزة في واتساب. تراجع الرسالة وتقرر إرسالها بنفسك. لا يستقبل الموقع بيانات النموذج أو يحتفظ بها.</p><h2>روابط الأطراف الأخرى</h2><p>قد تنقلك الروابط إلى واتساب أو إنستغرام أو صفحات المصادر. تطبق تلك الخدمات سياسات الخصوصية الخاصة بها.</p><h2>التواصل</h2><p>للاستفسار عن البيانات التي تشاركها مباشرة مع الأكاديمية، راسلها على info@muscatmusicartacademy.com.</p>'
    else:
        title='Privacy'; intro='This informational website does not create user accounts or store admissions enquiry details on its server.'
        body='<h2>Admissions enquiries</h2><p>When you complete the enquiry form, your browser prepares a WhatsApp message. You review it and decide whether to send it. The website does not receive or retain the form data.</p><h2>Third-party links</h2><p>Links may take you to WhatsApp, Instagram or source pages. Their own privacy policies apply.</p><h2>Contact</h2><p>For questions about information you share directly with the academy, email info@muscatmusicartacademy.com.</p>'
    return f'<section class="page-banner"><div class="container"><span class="eyebrow">PRIVACY / الخصوصية</span><h1>{title}</h1><p>{intro}</p></div></section><section class="section"><div class="container legal-copy">{body}</div></section>'

PAGES = {"index":home,"about":about,"programs":programs,"admissions":admissions,"news":news,"contact":contact,"privacy":privacy}
DESCRIPTIONS = {
    "ar": {"index":"أكاديمية مسقط للموسيقى والفنون: تعليم الموسيقى والفنون البصرية والباليه في شاطئ القرم، مسقط.","about":"تعرف إلى أكاديمية مسقط للموسيقى والفنون ومؤسسها الدكتورة شريفة اليحيائية.","programs":"استكشف مجالات الموسيقى والفنون البصرية والباليه والحركة في أكاديمية مسقط.","admissions":"خطوات الاستفسار والالتحاق بأكاديمية مسقط للموسيقى والفنون.","news":"أخبار وشراكات أكاديمية مسقط للموسيقى والفنون.","contact":"تواصل مع أكاديمية مسقط للموسيقى والفنون في شاطئ القرم.","privacy":"كيفية التعامل مع بيانات الاستفسارات في موقع أكاديمية مسقط للموسيقى والفنون."},
    "en": {"index":"Music, visual arts and ballet learning at Muscat Music & Art Academy, Shatti Al Qurum.","about":"Learn about Muscat Music & Art Academy and its founder Dr Sharifa Al Yahyai.","programs":"Explore music, visual arts, ballet and movement learning in Muscat.","admissions":"How to enquire about joining Muscat Music & Art Academy.","news":"News and partnerships of Muscat Music & Art Academy.","contact":"Contact Muscat Music & Art Academy in Shatti Al Qurum.","privacy":"How admissions enquiries are handled on the academy website."},
}

for lang in ("ar","en"):
    for key,render in PAGES.items():
        title=dict(NAV[lang]).get(key,TEXT[lang]["privacy"])
        content=page_head(key,lang,title,DESCRIPTIONS[lang][key])+render(lang)+page_foot(lang)
        output=DIST/path(key,lang)
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(content,encoding="utf-8")
        print(output.relative_to(ROOT))

(DIST/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(
    f'  <url><loc>{BASE}/{path(key,lang)}</loc></url>\n' for lang in ("ar","en") for key in PAGES
)+'</urlset>\n',encoding="utf-8")
(DIST/"robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n',encoding="utf-8")
(DIST/"manifest.webmanifest").write_text(json.dumps({
    "id":"/", "name":"أكاديمية مسقط للموسيقى والفنون | Muscat Music & Art Academy",
    "short_name":"أكاديمية مسقط", "start_url":"/", "scope":"/", "display":"standalone",
    "background_color":"#17211f", "theme_color":"#17211f", "lang":"ar",
    "icons":[
        {"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
        {"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"}
    ]
},ensure_ascii=False,indent=2),encoding="utf-8")
(DIST/"404.html").write_text(page_head("index","ar","الصفحة غير موجودة","الصفحة المطلوبة غير متاحة.")+
    '<section class="page-banner"><div class="container"><span class="eyebrow">404</span><h1>الصفحة غير موجودة</h1><p>قد يكون الرابط قد تغير. يمكنك العودة إلى الصفحة الرئيسية أو التواصل مع الأكاديمية.</p><a class="btn btn-gold" href="/index.html">العودة إلى الرئيسية</a></div></section>'+page_foot("ar"),encoding="utf-8")

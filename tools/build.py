#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an entirely static, dependency-free GitHub Pages website."""
import argparse
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'content/site.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--base', default=CONFIG['base_path'])
parser.add_argument('--output', default='dist')
args = parser.parse_args()
BASE = args.base.rstrip('/')
OUT = ROOT / args.output
OUT.mkdir(parents=True, exist_ok=True)
E = html.escape

def url(path=''):
    return BASE + '/' + path.lstrip('/')

def link(path, label, cls=''):
    return f'<a href="{E(url(path))}" class="{cls}">{label}</a>'

def issue(app=None):
    title = (app['name'] + '：') if app else 'お問い合わせ：'
    from urllib.parse import urlencode
    return 'https://github.com/' + CONFIG['repository'] + '/issues/new?' + urlencode({'title': title, 'body': '【お問い合わせ内容】\n\n【アプリのバージョン】\n\n【端末・OS】\n\n【発生した日時・路線・駅】\n\n※氏名・メールアドレス・現在地などの個人情報やAPIキーは記載しないでください。'})

TRAIN = '<svg viewBox="0 0 40 40" aria-hidden="true" fill="none"><rect x="9" y="6" width="22" height="25" rx="6" stroke="currentColor" stroke-width="2"/><path d="M10 19h20M14 12h12M14 35l3-4m9 4-3-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="15" cy="25" r="2" fill="currentColor"/><circle cx="25" cy="25" r="2" fill="currentColor"/></svg>'
APPS = {
 'jre': {'name':'JREアプリ','short':'JRE','color':'green','headline':'いつもの路線を、<br>もっと身近に。','intro':'JR東日本を中心に、列車位置、発車時刻、運行情報をひとつに。<br>毎日の移動に、知りたい情報を。','description':'JR東日本を中心に列車位置、駅の発車時刻、運行情報を確認できる、Shimayu開発の非公式アプリです。','section':'路線のいまから、<br>次の発車まで。','body':'列車の位置を眺める。最寄駅の発車時刻を調べる。乗換経路を探す。いつもの移動で確かめたいことを、iPhoneやApple Watchから確認できます。','features':[('列車の位置を、ひと目で。','JR東日本に加え、都営地下鉄・京急・東武・京王・横浜市営地下鉄の列車位置に対応。路線を選んで、公開されている列車の位置を確認できます。'),('発車時刻を、手元で。','駅や最寄駅の時刻表から、次の発車を確認。位置情報を許可すると、近くの駅を探す操作をサポートします。'),('経路も、運行情報も。','出発駅・到着駅を指定して経路を検索。JR東日本の運行情報も確認でき、移動前の情報収集に役立ちます。')],'coverage':['JR東日本','都営地下鉄','京急電鉄','東武鉄道','京王電鉄','横浜市営地下鉄'],'coverage_note':'列車位置の公開路線・区間は事業者によって異なります。対応範囲はアプリ内の路線選択と案内で確認できます。運行情報や経路検索は、列車位置と提供範囲が異なります。'},
 'yokohama': {'name':'横浜地下鉄アプリ','short':'横浜地下鉄','color':'blue','headline':'横浜の地下鉄を、<br>もっと軽やかに。','intro':'ブルーラインも、グリーンラインも。<br>列車位置と発車時刻を、すっきり確認。','description':'横浜市営地下鉄のブルーライン・グリーンラインの列車位置、運行情報、時刻表を確認できる、Shimayu開発の非公式アプリです。','section':'横浜を走る、<br>2つの路線と。','body':'ブルーラインとグリーンラインの列車位置、運行情報、駅の時刻表を確認。iPhone、Apple Watch、ウィジェットで、日々の移動をサポートします。','features':[('ブルーも、グリーンも。','横浜市営地下鉄のブルーライン・グリーンラインに対応。列車がどの駅の間を走っているか、路線上で確認できます。'),('最寄駅の、次の電車。','位置情報を許可すると、近くの駅を探せます。駅の時刻表や運行情報を確認し、お出かけ前の準備に。'),('手元でも、ホーム画面でも。','Apple Watchで情報を確認。ウィジェットには、iPhoneアプリで保存された駅の発車標を表示できます。')],'coverage':['ブルーライン','グリーンライン'],'coverage_note':'横浜市営地下鉄向けのアプリです。横浜市内を走るすべての鉄道に対応するものではありません。ウィジェットは保存済みの情報を利用するため、アプリ本体と表示の更新時刻が異なる場合があります。'}
}

def phone(color, mode='route'):
    key = 'jre' if color == 'green' else 'yokohama'
    app = APPS[key]
    return f'<div class="phone real-screen {color}"><img src="{url("assets/"+key+"-screen.png")}" alt="{app["name"]}の実際のアプリ画面" width="1206" height="2622" decoding="async"></div>'

def visual(key=None):
    phones = phone('green') + phone('blue','timetable') if key is None else phone(APPS[key]['color'], 'route' if key=='jre' else 'timetable')
    return f'<div class="product-visual" >{phones}</div>'

NOTE = '<p class="illustration-note">掲載画面はシミュレータで撮影した開発版です。表示内容は撮影時点のもので、公開版とは異なる場合があります。</p>'

def localnav(key, current):
    app=APPS[key]
    links=''
    for suffix,label in [('', '概要'),('support/','サポート'),('privacy/','プライバシー')]:
        path=f'{key}/'+suffix
        links+=f'<a href="{E(url(path))}"'+(' aria-current="page"' if current==path else '')+f'>{label}</a>'
    return '<div class="local-nav"><div class="wrap"><strong>'+app['name']+'</strong><nav class="local-nav-links" aria-label="アプリ内メニュー">'+links+'</nav></div></div>'

def page(path,title,description,body,key=None,noindex=False):
    links=''
    for target,label in [('jre/','JRE'),('yokohama/','横浜地下鉄'),('support/','サポート')]:
        links+=f'<a href="{E(url(target))}"'+(' aria-current="page"' if target==path else '')+f'>{label}</a>'
    footer=f'''<footer class="footer"><div class="wrap"><p class="footer-notes">本サイトは{E(CONFIG['developer'])}が開発するアプリの紹介・サポートサイトです。各アプリは非公式であり、鉄道会社・交通事業者およびAppleの公式アプリではありません。<br>列車位置や時刻表の表示には遅れ・誤差が生じる場合があります。最新の情報は駅の案内や各事業者の公式情報をご確認ください。</p><div class="footer-bottom"><span>© 2026 {E(CONFIG['developer'])}</span><div class="footer-links">{link('support/','お問い合わせ')}{link('privacy/','本サイトのプライバシー')}<a href="https://github.com/{E(CONFIG['repository'])}">GitHub</a></div></div></div></footer>'''
    canonical=CONFIG['origin']+url(path)
    doc=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{E(title)} | {E(CONFIG['title'])}</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{E(canonical)}"><meta property="og:type" content="website"><meta property="og:locale" content="ja_JP"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{E(canonical)}"><meta name="theme-color" content="#fafafc"><link rel="icon" href="{url('assets/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{url('assets/site.css')}">{'<meta name="robots" content="noindex">' if noindex else ''}</head><body><a class="skip" href="#main">本文へスキップ</a><header class="global-nav"><nav class="nav-inner" aria-label="メインメニュー"><a class="brand" href="{url()}">Shimayu<span>Apps</span></a><div class="nav-links">{links}</div></nav></header>{localnav(key,path) if key else ''}<main id="main" class="{'theme-'+APPS[key]['color'] if key else ''}">{body}</main>{footer}</body></html>'''
    target=OUT/(path+'index.html' if not path.endswith('.html') else path)
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc)
    return canonical

urls=[]
hero=f'''<section class="hero"><p class="eyebrow">Shimayu Apps</p><h1>次の電車が、<br>すぐわかる。</h1><p class="intro">いつもの駅も、はじめての路線も。<br><strong>毎日の移動に、ちょうどいいアプリを。</strong></p><div class="hero-actions"><a class="button" href="#apps">アプリを見る</a>{link('support/','サポートはこちら','text-link')}</div>{visual()}</section>{NOTE}'''
cards=''
for key,app in APPS.items():
    headline='路線のいまを、<br>ひと目で。' if key=='jre' else '横浜を走る、<br>あなたの手元で。'
    cards+=f'''<article class="product-panel panel-{app['color']}"><div class="product-copy"><div class="app-symbol">{TRAIN}</div><p class="device-note">iPhone / Apple Watch</p><h3>{app['name']}</h3><p>{'JR東日本を中心とした列車位置と発車時刻。<br>いつもの路線を、もっと身近に。' if key=='jre' else 'ブルーラインとグリーンライン。<br>列車位置も、駅の時刻表も、すっきり。'}</p>{link(key+'/', 'さらに詳しく','text-link')}</div>{visual(key)}</article>'''
helpblocks=f'''<section class="help-section wrap"><h2 class="section-heading">使うときも。<br>困ったときも。</h2><div class="help-grid"><div class="help-block"><h3>サポート</h3><p>使い方やよくある質問、不具合の連絡先をまとめました。アプリを選んでご確認ください。</p>{link('jre/support/','JREアプリ ›')}{link('yokohama/support/','横浜地下鉄アプリ ›')}</div><div class="help-block"><h3>プライバシー</h3><p>位置情報や外部サービスとの通信について、アプリごとに説明しています。</p>{link('jre/privacy/','JREアプリ ›')}{link('yokohama/privacy/','横浜地下鉄アプリ ›')}</div></div></section>'''
urls.append(page('','毎日の移動に、ちょうどいいアプリを。','Shimayuが開発するJREアプリ・横浜地下鉄アプリの紹介、サポート、プライバシーポリシー。',hero+'<section class="products wrap" id="apps"><h2 class="section-heading">あなたの路線に、<br>あなたのアプリを。</h2>'+cards+'</section>'+helpblocks))

for key,app in APPS.items():
    features=''.join(f'<article class="feature-item"><span class="feature-num">0{i+1}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(app['features']))
    coverage=''.join('<li>'+s+'</li>' for s in app['coverage'])
    body=f'''<section class="hero product-hero"><p class="eyebrow">{app['name']}</p><h1>{app['headline']}</h1><p class="intro">{app['intro']}</p><div class="hero-actions">{link(key+'/support/','使い方・サポート','button')}{link(key+'/privacy/','プライバシーについて','text-link')}</div>{visual(key)}</section>{NOTE}<section class="wrap"><div class="feature-intro"><h2 class="section-heading">{app['section']}</h2><p>{app['body']}</p></div><div class="feature-grid">{features}</div><section class="coverage"><h2>対応する路線・事業者</h2><ul class="line-list">{coverage}</ul><p>{app['coverage_note']}</p></section><section class="coverage"><h2>データ提供について</h2><p>公共交通オープンデータセンター（ODPT）を通じて提供されるデータを利用しています。提供元の更新や通信状況により、情報が遅れる場合があります。本アプリは鉄道会社・交通事業者とは独立して開発されています。</p><p><a href="https://www.odpt.org/">ODPTについて ›</a></p>{'<p>都営地下鉄のデータ提供：東京都交通局・公共交通オープンデータ協議会。対象データのライセンス：<a href="https://creativecommons.org/licenses/by/4.0/deed.ja">CC BY 4.0</a>。列車位置等を表示用に加工しています。</p>' if key=='jre' else ''}</section><section class="availability"><h2>アプリの公開情報</h2><p>App Storeへのリンク・公開版の対応OSは、<br>配信情報が確定し次第、このページでご案内します。</p>{link(key+'/support/','ご質問はこちら','text-link')}</section></section>'''
    urls.append(page(key+'/',app['name'],app['description'],body,key))

    faqs=[('列車位置が更新されない、または表示されません。','通信状態と、アプリで選んでいる路線をご確認ください。列車位置は提供元の情報を一定間隔で取得しているため、実際の位置と差が生じます。データ未提供の路線・区間や運行時間外には、列車が表示されない場合があります。'),('位置情報の許可は必要ですか？','近くの駅を探す機能で位置情報を利用します。iPhoneの「設定」→「プライバシーとセキュリティ」→「位置情報サービス」から許可を変更できます。駅・路線を手動で選ぶ機能は位置情報を許可せず利用できます。'),('駅の発車時刻と実際の発車時刻が違います。','時刻表・遅延情報の更新状況によって差が生じる場合があります。臨時運行やダイヤ変更がすぐに反映されないこともあります。乗車時は駅の発車標や係員の案内を優先してください。'),('Apple Watchで情報を取得できません。','Watchのインターネット接続を確認し、アプリを開き直してください。位置情報を利用する場合は、Watch側の許可設定も確認してください。改善しない場合は、端末とOS、操作手順を添えてご連絡ください。'),('鉄道会社の公式アプリですか？','いいえ。Shimayuが開発する非公式アプリです。鉄道会社・交通事業者に、本アプリの不具合や操作方法をお問い合わせいただくことはお控えください。')]
    if key=='yokohama': faqs.insert(3,('ウィジェットが古い情報を表示します。','ウィジェットはiPhoneアプリで保存された駅の発車標を利用します。iPhoneで対象の駅を表示し、ウィジェットを確認してください。iOSによる更新タイミングの制御があるため、常に最新とは限りません。'))
    if key=='jre': faqs.insert(3,('経路検索ができません。','通信状態と出発駅・到着駅の入力を確認してください。経路検索には外部サービスを利用しており、提供元の制限や障害により利用できない場合があります。別の駅の組み合わせでも発生する場合はご連絡ください。'))
    faqhtml=''.join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q,a in faqs)
    contact=f'<a class="button" href="{E(issue(app))}">GitHubで問い合わせる</a>'
    if CONFIG['contact_email']:
        contact=f'<a class="button" href="mailto:{E(CONFIG["contact_email"])}">メールで問い合わせる</a>'
    body=f'''<article class="document"><p class="eyebrow">{app['name']}</p><h1>サポート</h1><p class="lead">使い方のヒントと、よくあるご質問。<br>解決しないときは、開発者へご連絡ください。</p><div class="callout"><h2>お問い合わせ</h2><p>アプリの操作、不具合、ご要望を受け付けています。開発者：{E(CONFIG['developer'])}</p>{contact}<p><small>GitHub Issuesは公開されます。氏名・連絡先・現在地などの個人情報は記載しないでください。投稿にはGitHubアカウントが必要です。</small></p></div><h2>よくあるご質問</h2><div class="faq">{faqhtml}</div><h2>不具合をご連絡いただくとき</h2><p>確認をスムーズにするため、わかる範囲で次の情報をお知らせください。</p><ul><li>アプリ名・アプリのバージョン</li><li>端末名・iOSまたはwatchOSのバージョン</li><li>発生した日時、対象の路線・駅</li><li>行った操作、期待した動作、実際に起きたこと</li><li>可能であればスクリーンショット（個人情報は隠してください）</li></ul><h2>情報の取り扱いについて</h2><p>{link(key+'/privacy/','このアプリのプライバシーポリシー')}をご確認ください。</p><p class="updated">最終更新日：{CONFIG['updated']}</p></article>'''
    urls.append(page(key+'/support/',app['name']+'のサポート',app['name']+'のよくある質問、使い方、不具合報告とお問い合わせ先。',body,key))

    sections=[('scope','対象と運営者',f'本ポリシーは、{E(CONFIG["developer"])}（以下「開発者」）が提供する「{app["name"]}」における情報の取り扱いを説明するものです。Cloudflareを経由してODPTデータを取得する現行の開発版・対応版を対象とします。旧バージョンでは通信先や機能が異なる場合があります。'),('location','位置情報','最寄駅を探すため、利用者の許可に基づき端末の位置情報を利用します。最寄駅と現在地の距離の計算は端末上で行います。最寄駅の判定に用いる現在地の座標を、ODPT取得用の開発者サーバーへ送信する処理は設けていません。位置情報の許可は端末の設定から変更できます。'),('local','端末に保存する情報','表示設定、選択した駅・路線などを、設定の保持と機能の提供のため端末に保存します。'+('最近検索した駅・目的地も端末に保存します。' if key=='jre' else 'ウィジェット用の駅・発車標情報は、端末のApp Group領域で共有します。')+'これらを広告目的で利用する処理は設けていません。端末内の情報は、アプリの削除や端末側の設定により削除できます。バックアップ等の取り扱いはOSの設定に従います。'),('network','外部サービスとの通信','列車位置、運行情報、駅、時刻表等の取得に、Cloudflareと公共交通オープンデータセンター（ODPT）を利用します。要求には、表示対象の事業者、駅、路線、列車番号、カレンダー等の検索条件が含まれる場合があります。通信先のサービスは、接続元IPアドレス、要求日時、URL、端末の通信クライアント情報等を処理する場合があります。開発者のWorkerはODPTデータを共有キャッシュとして保存し、利用者ごとの現在地履歴を記録するための仕組みは設けていません。')]
    if key=='jre': sections.append(('route','経路検索について','経路検索にはRapidAPI経由のNAVITIME関連APIを利用します。指定した出発駅・到着駅の駅IDまたは駅の座標、出発・到着の希望日時等を送信します。駅名から座標を解決するため、AppleのMapKitサービスに駅名を送信する場合があります。ここで使用する駅の座標と、端末で取得する利用者の現在地とは異なります。各通信先ではIPアドレス等の通信情報も処理される場合があります。'))
    sections += [('tracking','広告・トラッキング','現行の確認対象実装では、広告配信用SDKや広告識別子による追跡を行う処理は導入していません。外部サービスによる通信情報の処理まで存在しないことを意味するものではありません。'),('retention','保存・削除について','開発者のサーバーに保存する共有キャッシュは、公共交通データとその取得時刻です。通信や障害対応に伴うログの保持・削除は、利用するホスティングサービスの設定やポリシーに従います。問い合わせに含まれる情報は、内容の確認と対応のために利用します。GitHub Issuesに投稿した内容の管理についてはGitHubの機能・規約に従います。'),('choices','利用者による選択','位置情報は端末の設定から許可・拒否を変更できます。外部への通信を希望しない場合は、端末の通信設定でアプリのネットワーク利用を制限するか、アプリの利用を停止してください。情報の取り扱いに関するご質問や削除のご相談は、サポート窓口にご連絡ください。'),('changes','変更とお問い合わせ',f'機能や利用サービスの変更に応じて本ポリシーを更新します。変更後の内容は本ページに掲載します。お問い合わせ先は{link(key+"/support/","サポートページ")}をご確認ください。開発者：{E(CONFIG["developer"])}。')]
    toc=''.join(f'<li><a href="#{id}">{heading}</a></li>' for id,heading,text in sections)
    sectionshtml=''.join(f'<section id="{id}"><h2>{i+1}. {heading}</h2><p>{text}</p></section>' for i,(id,heading,text) in enumerate(sections))
    external='<ul><li><a href="https://www.cloudflare.com/privacypolicy/">Cloudflareのプライバシーポリシー</a></li><li><a href="https://www.odpt.org/privacy-policy/">公共交通オープンデータ協議会のプライバシーポリシー</a></li>'
    if key=='jre': external+='<li><a href="https://corporate.navitime.co.jp/policy/privacypolicy.html">NAVITIMEのプライバシーポリシー</a></li><li><a href="https://rapidapi.com/page/privacy">Rapid APIのプライバシーに関する案内</a></li><li><a href="https://www.apple.com/legal/privacy/jp/">Appleのプライバシーポリシー</a></li>'
    external+='</ul>'
    body=f'<article class="document"><p class="eyebrow">{app["name"]}</p><h1>プライバシーポリシー</h1><p class="lead">利用する情報と、その目的について。</p><p class="updated">制定・最終更新日：{CONFIG["updated"]}</p><nav class="toc" aria-label="目次"><p>目次</p><ol>{toc}</ol></nav>{sectionshtml}<h2>外部サービスの案内</h2>{external}</article>'
    urls.append(page(key+'/privacy/',app['name']+'のプライバシーポリシー',app['name']+'で利用する位置情報、端末保存情報、外部サービスとの通信について。',body,key))

cards=''.join(f'<a class="support-card" href="{url(key+"/support/")}"><h2>{app["name"]}</h2><p>よくあるご質問・お問い合わせ ›</p></a>' for key,app in APPS.items())
body=f'<section class="document"><p class="eyebrow">Shimayu Apps</p><h1>サポート</h1><p class="lead">ご利用のアプリをお選びください。</p><div class="support-chooser">{cards}</div><h2>開発者について</h2><p>開発者：{E(CONFIG["developer"])}<br>アプリに関するお問い合わせは、各アプリのサポートページからご連絡ください。</p><p><a href="https://github.com/Shimayu13">GitHubプロフィール ›</a></p></section>'
urls.append(page('support/','サポート','JREアプリ・横浜地下鉄アプリのサポート窓口。',body))
body=f'''<article class="document"><p class="eyebrow">Shimayu Apps</p><h1>本サイトのプライバシー</h1><p class="lead">このWebサイトをご覧いただくときの情報の取り扱いです。<br>アプリのポリシーは、各アプリのページをご覧ください。</p><h2>サイトの配信</h2><p>本サイトはGitHub Pagesを利用した静的サイトです。独自のアクセス解析、広告、問い合わせフォーム、利用者アカウント機能は設けていません。閲覧者情報を保存する独自のCookieやローカルストレージは使用しません。外部フォントや外部スクリプトの読み込みも行いません。</p><h2>GitHubによる情報の処理</h2><p>ページの配信と安全な運用のため、GitHubがIPアドレスなどの通信情報を取り扱います。詳細は<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHubのプライバシーステートメント</a>をご確認ください。</p><h2>お問い合わせ</h2><p>GitHub Issuesへの投稿は公開されます。個人情報を投稿しないでください。投稿内容は問い合わせへの対応に利用します。{link('support/','サポート窓口')}をご利用ください。</p><h2>アプリのプライバシーポリシー</h2><ul><li>{link('jre/privacy/','JREアプリ')}</li><li>{link('yokohama/privacy/','横浜地下鉄アプリ')}</li></ul><p class="updated">開発者：{E(CONFIG['developer'])}<br>最終更新日：{CONFIG['updated']}</p></article>'''
urls.append(page('privacy/','本サイトのプライバシー','Shimayu AppsのWebサイトのプライバシーに関する説明。',body))
page('404.html','ページが見つかりません','お探しのページは見つかりませんでした。','<section class="error-page"><p class="eyebrow">お探しのページが見つかりません</p><h1>次の目的地へ。</h1><p>URLが変更されたか、ページが存在しない可能性があります。</p>'+link('','トップページへ','button')+'</section>',noindex=True)
(OUT/'assets').mkdir(exist_ok=True)
for asset in (ROOT/'assets').iterdir():
    if asset.is_file(): shutil.copyfile(asset, OUT/'assets'/asset.name)
(OUT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#1d1d1f"/><path d="M42 20H27c-10 0-10 12 0 12h10c10 0 10 12 0 12H22" fill="none" stroke="white" stroke-width="6" stroke-linecap="round"/></svg>')
(OUT/'.nojekyll').touch()
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+CONFIG['origin']+url('sitemap.xml')+'\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+E(u)+'</loc></url>' for u in urls)+'</urlset>')
(OUT/'app-store-urls.json').write_text(json.dumps({key:{'marketing_url':CONFIG['origin']+url(key+'/'),'support_url':CONFIG['origin']+url(key+'/support/'),'privacy_policy_url':CONFIG['origin']+url(key+'/privacy/')} for key in APPS},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(urls)+1} pages into {OUT}, base path: {BASE or "/"}')

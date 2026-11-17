# -*- coding: utf-8 -*-
"""Explicit English copy; fail builds when Japanese copy lacks a translation."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode

COPY = {}
def pairs(text):
    for line in text.strip().splitlines():
        source, target = line.split('\t', 1)
        COPY[source] = target

pairs('''2つの路線と。	Two lines.
2つの路線の、	Two lines.
App Storeへのリンク・公開版の対応OSは、	App Store links and supported OS versions
Apple Watchで情報を取得できません。	Information is not loading on Apple Watch.
GitHub Issuesは公開されます。氏名・連絡先・現在地などの個人情報は記載しないでください。投稿にはGitHubアカウントが必要です。	GitHub Issues are public. Do not include personal information such as your name, contact details or current location. A GitHub account is required to post.
GitHub Issuesへの投稿は公開されます。個人情報を投稿しないでください。投稿内容は問い合わせへの対応に利用します。	Posts on GitHub Issues are public. Do not post personal information. We use the information you submit to respond to your inquiry.
GitHubで問い合わせる	Contact us on GitHub
GitHubによる情報の処理	Information processed by GitHub
GitHubのプライバシーステートメント	GitHub Privacy Statement
GitHubプロフィール ›	GitHub profile ›
JR東日本	JR East
JR東日本を中心とした列車位置と発車時刻。	Train positions and departures, with a focus on JR East.
JR東日本を中心に、列車位置、発車時刻、運行情報をひとつに。	Train positions, departures and service updates, with a focus on JR East.
JR東日本を中心に列車位置、駅の発車時刻、運行情報を確認できる、Shimayu開発の非公式アプリです。	An independent app by Shimayu for train positions, station departures and service updates, with a focus on JR East.
ODPTについて ›	About ODPT ›
Rapid APIのプライバシーに関する案内	RapidAPI privacy information
Shimayu AppsのWebサイトのプライバシーに関する説明。	Privacy information for the Shimayu Apps website.
Shimayuが開発するJREアプリ・横浜地下鉄アプリの紹介、サポート、プライバシーポリシー。	Explore JRE and Yokohama Subway apps by Shimayu, with support and privacy information.
URLが変更されたか、ページが存在しない可能性があります。	The address may have changed, or this page may no longer exist.
Watchのインターネット接続を確認し、アプリを開き直してください。位置情報を利用する場合は、Watch側の許可設定も確認してください。改善しない場合は、端末とOS、操作手順を添えてご連絡ください。	Check your Watch's internet connection and reopen the app. If you use location features, check location permissions on the Watch too. If the problem continues, contact us with your device, OS version and steps to reproduce it.
。列車位置等を表示用に加工しています。	. Train position data and other data are adapted for display.
あなたのアプリを。	Your app.
あなたの路線に、	Your railway.
いいえ。Shimayuが開発する非公式アプリです。鉄道会社・交通事業者に、本アプリの不具合や操作方法をお問い合わせいただくことはお控えください。	No. This is an independent app developed by Shimayu. Please contact the developer, rather than railway or transit operators, about app issues or how to use it.
いつもの路線を、	Your everyday railway.
いつもの路線を、もっと身近に。	Your everyday railway, closer at hand.
いつもの駅も、はじめての路線も。	Familiar stations. New routes.
いまが見える。	See where trains are.
お問い合わせ	Contact
お探しのページが見つかりません	We couldn't find that page
お探しのページは見つかりませんでした。	The page you requested could not be found.
このWebサイトをご覧いただくときの情報の取り扱いです。	How information is handled when you visit this website.
このアプリのプライバシーポリシー	this app's privacy policy
ご利用のアプリをお選びください。	Choose your app.
ご質問はこちら	Have a question?
さらに詳しく	Learn more
すぐわかる。	At a glance.
ひと目で。	At a glance.
もっと身近に。	Closer at hand.
もっと軽やかに。	Travel with ease.
よくあるご質問	Frequently asked questions
よくあるご質問・お問い合わせ ›	FAQs and contact ›
をご利用ください。	 for help.
をご確認ください。	 for more information.
をご確認ください。開発者：Shimayu。	. Developer: Shimayu.
アプリに関するお問い合わせは、各アプリのサポートページからご連絡ください。	For app inquiries, use the support page for the app you use.
アプリのプライバシーポリシー	App privacy policies
アプリのポリシーは、各アプリのページをご覧ください。	For app privacy policies, visit each app's page.
アプリの公開情報	App availability
アプリの操作、不具合、ご要望を受け付けています。開発者：Shimayu	Questions, bug reports and suggestions are welcome. Developer: Shimayu.
アプリを見る	Explore the apps
アプリ内メニュー	App navigation
アプリ名・アプリのバージョン	App name and version
ウィジェットが古い情報を表示します。	The widget shows outdated information.
ウィジェットはiPhoneアプリで保存された駅の発車標を利用します。iPhoneで対象の駅を表示し、ウィジェットを確認してください。iOSによる更新タイミングの制御があるため、常に最新とは限りません。	The widget uses station departure information saved by the iPhone app. Open the station in the iPhone app, then check the widget. iOS controls refresh timing, so widget information may not always be current.
グリーンライン	Green Line
サイトの配信	Website hosting
サポート	Support
サポートはこちら	Get support
サポートページ	support page
サポート窓口	our support pages
データ提供について	Data sources
トップページへ	Back to home
ブルーライン	Blue Line
ブルーラインとグリーンライン。	Blue Line and Green Line.
ブルーラインとグリーンラインの列車位置、運行情報、駅の時刻表を確認。iPhone、Apple Watch、ウィジェットで、日々の移動をサポートします。	Check train positions, service updates and station timetables for the Blue Line and Green Line. Plan everyday journeys with iPhone, Apple Watch and widgets.
ブルーラインの列車位置	Blue Line train positions
ブルーラインの列車詳細	Blue Line train details
ブルーラインも、グリーンラインも。	Blue Line. Green Line. Both at hand.
プライバシー	Privacy
プライバシーについて	About privacy
プライバシーポリシー	Privacy Policy
ページが見つかりません	Page not found
ページの配信と安全な運用のため、GitHubがIPアドレスなどの通信情報を取り扱います。詳細は	GitHub processes connection information, including IP addresses, to deliver pages and operate the service securely. See the 
ホーム・発車標	Home and departures
メインメニュー	Main navigation
不具合をご連絡いただくとき	Reporting a problem
乗る前に。	Before you board.
乗車中も。	Along the way.
乗車位置の共有も。	Share your car.
乗車位置を選んで、共有の準備を。	Choose your car and get ready to share.
京急電鉄	Keikyu
京王電鉄	Keio
位置情報	Location information
位置情報の許可は必要ですか？	Do I need to allow location access?
位置情報は端末の設定から許可・拒否を変更できます。外部への通信を希望しない場合は、端末の通信設定でアプリのネットワーク利用を制限するか、アプリの利用を停止してください。情報の取り扱いに関するご質問や削除のご相談は、サポート窓口にご連絡ください。	You can allow or deny location access in device settings. If you do not want the app to communicate with external services, restrict its network access in device settings or stop using it. Contact support with questions about information handling or deletion.
位置情報や外部サービスとの通信について、アプリごとに説明しています。	Read how each app uses location information and communicates with external services.
何号車にいるか、伝わる。	Let them know your car.
使い方のヒントと、よくあるご質問。	Helpful tips and answers to common questions.
使い方やよくある質問、不具合の連絡先をまとめました。アプリを選んでご確認ください。	Find tips, frequently asked questions and a way to report issues. Choose your app to get started.
使うときも。	Getting started.
保存・削除について	Retention and deletion
停車駅も。	And every stop.
公共交通オープンデータセンター（ODPT）を通じて提供されるデータを利用しています。提供元の更新や通信状況により、情報が遅れる場合があります。本アプリは鉄道会社・交通事業者とは独立して開発されています。	Uses data provided through the Public Transportation Open Data Center (ODPT). Information may be delayed by provider updates or connection conditions. This app is developed independently of railway and transit operators.
公共交通オープンデータ協議会のプライバシーポリシー	Association for Open Data of Public Transportation privacy policy
列車のいまが、見える。	See where trains are.
列車のいまを、	Where is your train?
列車の位置を眺める。最寄駅の発車時刻を調べる。乗換経路を探す。いつもの移動で確かめたいことを、iPhoneやApple Watchから確認できます。	See train positions, check departures at nearby stations and search for a route. Find the information you need for everyday travel on iPhone or Apple Watch.
列車の詳細	Train details
列車の詳細も。	Know your train.
列車を選ぶと、現在の走行位置、行き先、提供される遅延情報や停車駅の時刻を確認できます。	Select a train to see its position, destination, available delay information and times at its stops.
列車位置	Train positions
列車位置、運行情報、駅、時刻表等の取得に、Cloudflareと公共交通オープンデータセンター（ODPT）を利用します。要求には、表示対象の事業者、駅、路線、列車番号、カレンダー等の検索条件が含まれる場合があります。通信先のサービスは、接続元IPアドレス、要求日時、URL、端末の通信クライアント情報等を処理する場合があります。開発者のWorkerはODPTデータを共有キャッシュとして保存し、利用者ごとの現在地履歴を記録するための仕組みは設けていません。	The app uses Cloudflare and the Public Transportation Open Data Center (ODPT) to retrieve train positions, service updates, stations and timetables. Requests may include filters such as operator, station, line, train number and calendar. These services may process your IP address, request time, URL and network client information. The developer's Worker stores ODPT data in a shared cache; it has no mechanism designed to record each user's location history.
列車位置が更新されない、または表示されません。	Train positions are missing or not updating.
列車位置と発車時刻を、すっきり確認。	Train positions and departures, clearly presented.
列車位置の公開路線・区間は事業者によって異なります。対応範囲はアプリ内の路線選択と案内で確認できます。運行情報や経路検索は、列車位置と提供範囲が異なります。	Available train position data varies by operator, line and section. Check the line selection and information in the app for coverage. Service updates and route search have different coverage from train positions.
列車位置も、駅の時刻表も、すっきり。	Train positions and station timetables, clearly presented.
列車位置や時刻表の表示には遅れ・誤差が生じる場合があります。最新の情報は駅の案内や各事業者の公式情報をご確認ください。	Train positions and timetables may be delayed or inaccurate. For the latest information, follow station announcements and official operator information.
列車詳細と、乗車位置を共有する画面	Train details and sharing your train car screen
列車詳細・乗車位置の共有	Train details and sharing your train car
利用する情報と、その目的について。	What information is used, and why.
利用者による選択	Your choices
制定・最終更新日：2026年11月15日	Effective and last updated: November 15, 2026
可能であればスクリーンショット（個人情報は隠してください）	Screenshots if possible, with personal information hidden
困ったときも。	Getting help.
変更とお問い合わせ	Changes and contact
外部サービスとの通信	Communication with external services
外部サービスの案内	External service information
対応する路線・事業者	Supported lines and operators
対象と運営者	Scope and developer
少し先の予定も、	Planning ahead?
山手線の列車位置	Yamanote Line train positions
山手線の駅時刻表	Yamanote Line station timetable
平日・休日を切り替えて、駅の時刻表を確認。発車したい時間帯から電車を探せます。	Switch between weekday and holiday timetables to find a train for your preferred departure time.
広告・トラッキング	Advertising and tracking
待ち合わせに。	Meeting someone?
情報の取り扱いについて	How information is handled
戸塚駅の休日時刻表	Totsuka Station holiday timetable
戸塚駅の運行情報と発車標	Totsuka Station service updates and departures
掲載画面は実機・シミュレータで撮影したアプリの画面です。表示内容は撮影時点のもので、公開版とは異なる場合があります。	Screenshots were captured on devices and simulators. Information reflects the time of capture and may differ from the released app. Screenshots show the Japanese interface; this English website does not indicate English-language support in the apps.
方面と平日・休日を切り替えて、駅の時刻表を確認。次の一本だけでなく、出発したい時間帯の電車も探せます。	Choose a direction and switch between weekday and holiday timetables. Find the next train or plan a departure later in the day.
時刻・行き先・運行情報を一緒に確認。	Times, destinations and service updates in one place.
時刻表で。	Check the timetable.
時刻表・遅延情報の更新状況によって差が生じる場合があります。臨時運行やダイヤ変更がすぐに反映されないこともあります。乗車時は駅の発車標や係員の案内を優先してください。	Timetable and delay updates can cause differences. Extra services and schedule changes may not appear immediately. When travelling, follow station departure boards and staff guidance.
最寄駅を探すため、利用者の許可に基づき端末の位置情報を利用します。最寄駅と現在地の距離の計算は端末上で行います。最寄駅の判定に用いる現在地の座標を、ODPT取得用の開発者サーバーへ送信する処理は設けていません。位置情報の許可は端末の設定から変更できます。	With your permission, the app uses device location to find nearby stations. Distances between your location and stations are calculated on the device. The app has no process that sends the current-location coordinates used to find nearby stations to the developer's ODPT server. You can change location permissions in device settings.
最終更新日：2026年11月15日	Last updated: November 15, 2026
本サイトのプライバシー	Website Privacy
本サイトはGitHub Pagesを利用した静的サイトです。独自のアクセス解析、広告、問い合わせフォーム、利用者アカウント機能は設けていません。閲覧者情報を保存する独自のCookieやローカルストレージは使用しません。外部フォントや外部スクリプトの読み込みも行いません。	This is a static website hosted on GitHub Pages. It has no custom analytics, advertising, contact forms or user accounts. It does not use custom cookies or local storage to save visitor information, or load external fonts or scripts.
本サイトはShimayuが開発するアプリの紹介・サポートサイトです。各アプリは非公式であり、鉄道会社・交通事業者およびAppleの公式アプリではありません。	This website introduces and supports apps developed by Shimayu. The apps are independent and are not official apps of railway companies, transit operators or Apple.
本文へスキップ	Skip to content
東武鉄道	Tobu Railway
概要	Overview
横浜の地下鉄を、	Yokohama Subway.
横浜を走る、	Across Yokohama.
横浜地下鉄	Yokohama Subway
横浜市営地下鉄	Yokohama Municipal Subway
横浜市営地下鉄のブルーライン・グリーンラインの列車位置、運行情報、時刻表を確認できる、Shimayu開発の非公式アプリです。	An independent app by Shimayu for Blue Line and Green Line train positions, service updates and timetables on Yokohama Municipal Subway.
横浜市営地下鉄向けのアプリです。横浜市内を走るすべての鉄道に対応するものではありません。ウィジェットは保存済みの情報を利用するため、アプリ本体と表示の更新時刻が異なる場合があります。	Designed for Yokohama Municipal Subway, rather than every railway in Yokohama. Widgets use saved information and may show a different update time from the app.
横浜駅の発車標と運行情報	Yokohama Station departures and service updates
機能や利用サービスの変更に応じて本ポリシーを更新します。変更後の内容は本ページに掲載します。お問い合わせ先は	We update this policy as features or services change and publish the revised policy on this page. Contact details are on the 
機能を見てみる	Explore features
機能を見る	Explore features
次の発車まで。	To your next departure.
次の発車も。	Your next departure.
次の目的地へ。	On to your next stop.
次の電車が、	Your next train.
次の電車へ。	Your next train.
次の電車を、ひと目で。	Your next train, at a glance.
毎日の移動に、ちょうどいいアプリを。	The right apps for everyday travel.
毎日の移動に、知りたい情報を。	The information you need for everyday travel.
現行の確認対象実装では、広告配信用SDKや広告識別子による追跡を行う処理は導入していません。外部サービスによる通信情報の処理まで存在しないことを意味するものではありません。	The implementation reviewed does not include advertising SDKs or tracking through advertising identifiers. This does not mean external services do not process connection information.
画面をタップすると拡大できます。	Tap a screenshot to view it full size.
発生した日時、対象の路線・駅	Date and time, and the affected line or station
発車前に。	Before departure.
発車標・運行情報	Departures and service updates
目次	Contents
知りたいことが、画面を見ればわかる。	The information you need, right on screen.
確認をスムーズにするため、わかる範囲で次の情報をお知らせください。	To help us investigate, include as much of the following as you can.
移動の前も。	Before you go.
端末に保存する情報	Information stored on your device
端末名・iOSまたはwatchOSのバージョン	Device model and iOS or watchOS version
経路検索ができません。	Route search is not working.
経路検索について	Route search
経路検索にはRapidAPI経由のNAVITIME関連APIを利用します。指定した出発駅・到着駅の駅IDまたは駅の座標、出発・到着の希望日時等を送信します。駅名から座標を解決するため、AppleのMapKitサービスに駅名を送信する場合があります。ここで使用する駅の座標と、端末で取得する利用者の現在地とは異なります。各通信先ではIPアドレス等の通信情報も処理される場合があります。	Route search uses NAVITIME-related APIs through RapidAPI. It sends the selected departure and arrival station IDs or station coordinates, preferred departure or arrival dates and times, and related search parameters. Station names may be sent to Apple's MapKit service to resolve station coordinates. These station coordinates are different from your current device location. Each service may also process connection information such as IP addresses.
行き先、現在位置、停車駅を詳しく確認。乗車位置の共有画面では号車を選び、駅名と乗車位置を伝える準備ができます。共有先は送信前に選べます。	See the destination, current position and stops. On the sharing screen, choose a car to prepare to share the station and your position on the train. Choose who to share with before sending.
行き先も、	Your destination.
行った操作、期待した動作、実際に起きたこと	Steps taken, expected behaviour and what actually happened
解決しないときは、開発者へご連絡ください。	If you still need help, contact the developer.
路線のいまから、	From train positions.
近くの駅の、	A nearby station.
近くの駅を探す機能で位置情報を利用します。iPhoneの「設定」→「プライバシーとセキュリティ」→「位置情報サービス」から許可を変更できます。駅・路線を手動で選ぶ機能は位置情報を許可せず利用できます。	Location is used to find nearby stations. Change access in iPhone Settings → Privacy & Security → Location Services. You can select stations and lines manually without allowing location access.
通信状態と、アプリで選んでいる路線をご確認ください。列車位置は提供元の情報を一定間隔で取得しているため、実際の位置と差が生じます。データ未提供の路線・区間や運行時間外には、列車が表示されない場合があります。	Check your connection and the selected line. Train positions are retrieved at intervals and may differ from actual positions. Trains may not appear on lines or sections without data, or outside operating hours.
通信状態と出発駅・到着駅の入力を確認してください。経路検索には外部サービスを利用しており、提供元の制限や障害により利用できない場合があります。別の駅の組み合わせでも発生する場合はご連絡ください。	Check your connection and the departure and arrival stations. Route search uses external services and may be unavailable because of provider limits or outages. Contact us if the problem also occurs with other station pairs.
運行の変化も。	Service changes, too.
運行情報と、方面ごとの発車時刻をまとめて表示。種別や行き先、提供される遅延情報も、発車前に確認できます。	See service updates and departures by direction together. Check service types, destinations and available delay information before you board.
都営地下鉄	Toei Subway
都営地下鉄のデータ提供：東京都交通局・公共交通オープンデータ協議会。対象データのライセンス：	Toei Subway data: Bureau of Transportation, Tokyo Metropolitan Government, and Association for Open Data of Public Transportation. Applicable data licence: 
配信情報が確定し次第、このページでご案内します。	will be listed here once release information is confirmed.
鉄道会社の公式アプリですか？	Is this an official railway app?
開発者について	About the developer
開発者のサーバーに保存する共有キャッシュは、公共交通データとその取得時刻です。通信や障害対応に伴うログの保持・削除は、利用するホスティングサービスの設定やポリシーに従います。問い合わせに含まれる情報は、内容の確認と対応のために利用します。GitHub Issuesに投稿した内容の管理についてはGitHubの機能・規約に従います。	The shared cache on the developer's server contains public transportation data and retrieval times. Retention and deletion of connection or troubleshooting logs follow the hosting service's settings and policies. Information in inquiries is used to investigate and respond. Posts on GitHub Issues are managed according to GitHub's features and terms.
開発者：Shimayu	Developer: Shimayu
駅と駅の間を走る列車を、路線の流れに沿って表示。ブルーライン・グリーンラインを選んで、公開されている列車の位置を確認できます。	See trains between stations along the line. Select the Blue Line or Green Line to view publicly available train positions.
駅と駅の間を走る列車を路線上で。	See trains between stations on the line.
駅の時刻表	Station timetables
駅の発車時刻と実際の発車時刻が違います。	Departure times differ from actual departures.
駅の発車標では、行き先や発車時刻、提供される遅延情報をまとめて確認。移動前に確かめたい情報を、ひとつの画面に。	See destinations, departure times and available delay information on a station's departure board. Everything to check before travelling, in one view.
駅名と列車の位置を路線上に表示。走行中か、駅に停車しているかも確認できます。気になる列車を選ぶと、その列車の詳しい情報へ。	See station names and train positions along a line, including whether a train is moving or stopped at a station. Select a train to see more details.''')

for jp,en in [('JREアプリ','JRE App'),('横浜地下鉄アプリ','Yokohama Subway App')]:
    COPY[jp]=en
    COPY[jp+' ›']=en+' ›'
    COPY[jp+'のアイコン']=en+' icon'
    COPY[jp+'のサポート']=en+' Support'
    COPY[jp+'のプライバシーポリシー']=en+' Privacy Policy'
    COPY[jp+'で利用する位置情報、端末保存情報、外部サービスとの通信について。']='How '+en+' uses location information, local storage and external services.'
    COPY[jp+'のよくある質問、使い方、不具合報告とお問い合わせ先。']='FAQs, usage tips, bug reports and contact information for '+en+'.'
    COPY['本ポリシーは、Shimayu（以下「開発者」）が提供する「'+jp+'」における情報の取り扱いを説明するものです。Cloudflareを経由してODPTデータを取得する現行の開発版・対応版を対象とします。旧バージョンでは通信先や機能が異なる場合があります。']='This policy explains how information is handled in '+en+', provided by Shimayu (the developer). It covers the current development and supported versions that retrieve ODPT data through Cloudflare. Older versions may use different services or features.'
COPY['JREアプリ・横浜地下鉄アプリのサポート窓口。']='Support for JRE App and Yokohama Subway App.'
for extra,translation in [('最近検索した駅・目的地も端末に保存します。','Recently searched stations and destinations are also stored on the device.'),('ウィジェット用の駅・発車標情報は、端末のApp Group領域で共有します。','Station and departure information for widgets is shared through the device’s App Group storage.')]:
    COPY['表示設定、選択した駅・路線などを、設定の保持と機能の提供のため端末に保存します。'+extra+'これらを広告目的で利用する処理は設けていません。端末内の情報は、アプリの削除や端末側の設定により削除できます。バックアップ等の取り扱いはOSの設定に従います。']='Display preferences, selected stations and lines, and similar settings are stored on your device to retain preferences and provide features. '+translation+' The app has no process that uses this information for advertising. Local information can be removed by deleting the app or through device settings. Backups are handled according to OS settings.'
for jp,en in [('Apple','Apple'),('Cloudflare','Cloudflare'),('NAVITIME','NAVITIME')]:
    COPY[jp+'のプライバシーポリシー']=en+' privacy policy'

SCREENS={'山手線の列車位置':'Yamanote Line train positions','JREアプリ・横浜駅の発車標':'JRE App — Yokohama Station departures','JREアプリ・列車詳細':'JRE App — train details','JREアプリ・乗車位置を共有':'JRE App — share your car','JREアプリ・山手線の駅時刻表':'JRE App — Yamanote Line timetable','横浜地下鉄アプリ・ブルーラインの列車位置':'Yokohama Subway App — Blue Line train positions','横浜地下鉄アプリ・戸塚駅の発車標':'Yokohama Subway App — Totsuka Station departures','横浜地下鉄アプリ・列車詳細':'Yokohama Subway App — train details','横浜地下鉄アプリ・戸塚駅の時刻表':'Yokohama Subway App — Totsuka Station timetable'}
for jp,en in SCREENS.items():
    COPY[jp+'の実際のアプリ画面']=en+' screenshot (Japanese interface)'
    for mode,label in [('ライト','light'),('ダーク','dark')]:COPY[jp+'の'+mode+'画面を拡大する']='Enlarge '+en+' — '+label+' mode'

def translate(value):
    if value in COPY:return COPY[value]
    if not re.search('[ぁ-龯]',value):return value
    if value.endswith(' | Shimayu Apps'):return translate(value[:-len(' | Shimayu Apps')])+' | Shimayu Apps'
    match=re.match(r'(\d+\. )(.*)',value)
    if match:return match[1]+translate(match[2])
    raise ValueError('Missing English translation: '+repr(value))

class English(HTMLParser):
    def __init__(self,base,origin):super().__init__(convert_charrefs=True);self.parts=[];self.base=base;self.origin=origin
    def handle_decl(self,d):self.parts.append('<!'+d+'>')
    def handle_starttag(self,tag,attrs):
        result=[]
        for k,v in attrs:
            if k=='lang':v='en'
            elif k=='content' and v=='ja_JP':v='en_US'
            elif k in ('alt','aria-label','content'):v=translate(v) if v else v
            if k in ('href','content') and v:
                # Assets remain shared. Page links stay in English, including canonical/OG URLs.
                origin=self.origin
                prefix=origin if v.startswith(origin) else ''
                local=v[len(prefix):]
                if local.startswith(self.base+'/') and not local.startswith(self.base+'/assets/'):
                    v=prefix+self.base+'/en/'+local[len(self.base)+1:]
            if k=='href' and v and '/issues/new?' in v:
                v=v.split('?')[0]+'?'+urlencode({'title':'App support: ','body':'App and version:\n\nDevice and OS:\n\nDate, line and station:\n\nSteps, expected behaviour and actual result:\n\nDo not include personal information or API keys.'})
            result.append(k if v is None else k+'="'+html.escape(v,quote=True)+'"')
        self.parts.append('<'+tag+(' '+' '.join(result) if result else '')+'>')
    def handle_endtag(self,t):self.parts.append('</'+t+'>')
    def handle_data(self,d):self.parts.append(html.escape(translate(d)))

def generate(out,base,origin):
    originals=list(out.rglob('*.html'))
    english_urls=[]
    for source in originals:
        if 'en' in source.relative_to(out).parts:continue
        relative=source.relative_to(out)
        path='' if str(relative)=='index.html' else str(relative).removesuffix('index.html')
        ja=origin+base+'/'+path
        en=origin+base+'/en/'+path
        parser=English(base,origin);parser.feed(source.read_text())
        english=''.join(parser.parts)
        english=re.sub(r'(<p>)(<a href="[^"]+">this app)',r'\1See \2',english)
        english=english.replace('respond to your inquiry.<a', 'respond to your inquiry. Use <a')
        alternates=f'<link rel="alternate" hreflang="ja" href="{ja}"><link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="x-default" href="{ja}">'
        # Switch to the equivalent page, without automatic redirects or scripts.
        for content,dest,label,lang in [(source.read_text(),source,'English','en'),(english,out/'en'/relative,'日本語','ja')]:
            switch=f'<a class="language-switch" href="{base}/{"en/" if lang=="en" else ""}{path}" lang="{lang}" hreflang="{lang}" aria-label="{label}">{label}</a>'
            content=content.replace('</head>',alternates+'</head>').replace('</div></nav></header>',switch+'</div></nav></header>')
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content)
        if relative.name!='404.html':english_urls.append(en)
    return english_urls

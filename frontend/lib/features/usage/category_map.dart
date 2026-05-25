/// 패키지명 → 카테고리 매핑 (ARCHITECTURE 5종: sns/shorts/game/webtoon/other).
///
/// 본인이 ICP — 한국 1인 워커가 실제로 시간을 흘리는 앱 위주.
/// 동적 확장(웹툰 신규 등)은 firebase_remote_config로 W6에 보강 예정.
library;

/// 정확 매칭 우선 테이블.
const Map<String, String> _exact = {
  // SNS
  'com.instagram.android': 'sns',
  'com.twitter.android': 'sns',
  'com.zhiliaoapp.musically': 'shorts', // TikTok = 쇼츠
  'com.facebook.katana': 'sns',
  'com.linkedin.android': 'sns',
  'com.snapchat.android': 'sns',
  'com.pinterest': 'sns',
  'com.reddit.frontpage': 'sns',
  'com.thingsflow.android': 'sns', // 후후/커뮤니티류 예시
  // 쇼츠 / 동영상
  'com.google.android.youtube': 'shorts', // YouTube (쇼츠 비중 큼)
  'com.google.android.apps.youtube.music': 'other',
  'com.netflix.mediaclient': 'other',
  // 게임
  'com.supercell.clashofclans': 'game',
  'com.nianticlabs.pokemongo': 'game',
  'com.kakaogames.lqp': 'game',
  'com.ncsoft.lineagem19': 'game',
  // 웹툰
  'com.nhn.android.webtoon': 'webtoon', // 네이버 웹툰
  'com.kakao.page': 'webtoon', // 카카오페이지
  'com.kakaoent.leafon': 'webtoon', // 카카오웹툰
  'net.daum.android.webtoon': 'webtoon',
  'com.lezhin.comics': 'webtoon',
};

/// 부분 매칭 키워드 (패키지명에 포함되면 해당 카테고리).
const Map<String, String> _contains = {
  'webtoon': 'webtoon',
  'comics': 'webtoon',
  'game': 'game',
  'games': 'game',
  'shorts': 'shorts',
  'tiktok': 'shorts',
};

/// 패키지명을 카테고리로. 알 수 없으면 null (= 추적 대상 아님, 저장 안 함).
String? categoryForPackage(String packageName) {
  final exact = _exact[packageName];
  if (exact != null) return exact;

  final lower = packageName.toLowerCase();
  for (final entry in _contains.entries) {
    if (lower.contains(entry.key)) return entry.value;
  }
  return null;
}

# Design System — 끊기 (Kkeugi)

> /design-consultation 결과 · 2026-05-22 · DRAFT v1
> 본인이 ICP, design doc: `~/.gstack/projects/kkeugi/jungsunpark-main-design-20260522-001310.md`

## Memorable Thing

**거울 같은 친구 — 압박 X, 비난 X, 객관 O, 지속 동기.**

> "압박하지 않고, 비난하지 않지만, 객관적으로 나를 평가할 수 있도록. 집중해야 한다는 느낌을 지속적으로 동기부여한다."
> — 본인 (ICP), 2026-05-22

이 한 문장이 모든 디자인 결정의 기준이다. 새 컴포넌트·카피·색을 추가할 때 이 4축 (압박 X · 비난 X · 객관 O · 지속)으로 self-check.

## Product Context

- **What this is**: 한국 1인 워커용 디지털 디톡스 Android 앱 (Flutter, Material 3)
- **Who it's for**: 1인 워커 (개발자·디자이너·작가·연구자·프리·1인 사업자), 본인 ICP
- **Space/industry**: 디지털 디톡스 + Focus Accountant vertical (Opal·Forest·간단 인접)
- **Project type**: 모바일 앱 (Android 단일 시드, iOS v2)
- **Language**: 한국어 primary, English/숫자 보조

## Aesthetic Direction

- **Direction**: Brutally minimal + 한국 정서 ma (간격)
- **Decoration level**: minimal — typography does all the work
- **Mood**: 거울 같은 친구 — 어른의 도구. 따뜻하지만 친근한 척하지 않음.
- **Reference apps**: 토스 (numeric authority), Linear (quiet motivation), Things 3 (typographic hierarchy), 간단 (Korean indie restraint)
- **Anti-pattern**: Forest 게임화, Opal purple gradient, Kakao mascot warmth, 3-column SaaS grid

## Typography

### Loading
- **Pretendard Variable** — `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.css` (Flutter: pretendard pub package 또는 fonts/Pretendard-Variable.ttf bundle)
- **IBM Plex Mono** — Google Fonts (Flutter: google_fonts package, weights 400/500/600)

### Roles

| 역할 | 폰트 | 가중치 | 크기 | letter-spacing |
|---|---|---|---|---|
| Hero numeral (₩·시간 빚) | **IBM Plex Mono** | 600 | 64-80sp | -0.02em, `tabular-nums` |
| Display (앱명·section title) | Pretendard | 700 | 56-72sp | -0.03em |
| H2 (화면 제목) | Pretendard | 600 | 28-32sp | -0.02em |
| H3 (sub-section) | Pretendard | 600 | 18-20sp | -0.01em |
| Body | Pretendard | 400 | 15-16sp | 0, line-height 1.6 |
| Body small (보조) | Pretendard | 400 | 13-14sp | 0 |
| Label · UPPERCASE | IBM Plex Mono | 400 | 11-12sp | 0.05-0.08em uppercase |

### Rules

- **Hero numeral만 IBM Plex Mono**, 나머지 모든 Hangul은 Pretendard. 두 폰트만 사용.
- **`tabular-nums` 모든 숫자 표시에 강제** (시간·분·원 단위)
- **Serif 절대 금지** — 디톡스 카테고리 전체에 serif 0
- **font-feature-settings: "ss06", "ss07"** (Pretendard 옵션 ligatures)
- **System fallback**: `-apple-system, BlinkMacSystemFont, system-ui, Roboto`

### Hangul-specific

- 한글 본문 14sp 미만 금지 (가독성 floor)
- 한글 letter-spacing 절대 양수 금지 (Pretendard 기본값 사용)
- 영문·숫자 letter-spacing은 -0.01 ~ -0.03em (display) / 0 (body)

## Color

### Palette

| 토큰 | Hex | 역할 |
|---|---|---|
| `--bg` | `#FAFAF7` | 본 화면 배경 (warm off-white, not cool gray) |
| `--surface` | `#FFFFFF` | 카드·입력 필드 배경 |
| `--surface-2` | `#F5F2EC` | 미묘한 그룹핑 배경 |
| `--text-primary` | `#1A1A1A` | 본문, hero numeral default |
| `--text-secondary` | `#8A8A85` | 보조 설명·레이블 (warm gray) |
| `--text-tertiary` | `#BCBBB7` | 가장 약한 텍스트·placeholder |
| `--accent` | `#8B5A3C` | clay · link · 활성 ring · 매출 환산 hero |
| `--accent-soft` | `#E8DDD4` | accent 배경 tint (드물게) |
| `--divider` | `#E8E5DE` | 보더·구분선 |
| `--success` | `#2E4A3F` | deep ink-green · 회복·진행 |
| `--danger` | `#8B3C3C` | muted red · 권한 거부·에러 (드물게) |

### Approach

- **restrained**: 4-5 회색 + 단일 warm accent (clay)
- **다중 색 절대 금지** — semantic colors도 모두 muted/desaturated
- **Accent 사용처 제한**:
  - hero numeral (매출 환산 모드일 때만)
  - 활성 timer ring (V1)
  - text-only link
  - 권한 동의 화면 작은 dot
- **카테고리에 비어있는 색**: Toss blue · Kakao yellow · 간단 mint · Linear lime · Things blue — kkeugi는 clay로 차지

### Dark mode

- **V2** — Phase 1 매출 ₩200만/월 이후. Light 우선 ship.
- v2 진입 시 saturation 10-15% 줄이고 contrast 재조정. 단순 invert 금지.

## Spacing

- **Base unit**: 4px
- **Density**: comfortable (Korean text-heavy)
- **Scale**:

| 토큰 | px |
|---|---|
| `xs` | 4 |
| `sm` | 8 |
| `md` | 16 |
| `lg` | 24 |
| `xl` | 32 |
| `2xl` | 48 |
| `3xl` | 64 |
| `4xl` | 96 |

- 화면 padding: 16-24sp (mobile)
- Section vertical 간격: 32-48sp
- Component 내부 padding: 16sp default

## Layout

- **Approach**: grid-disciplined + one hero numeral per screen
- **Mobile**: single column, 16sp horizontal padding
- **모든 화면 규칙**: 가장 큰 시각 요소 = 단 하나의 숫자
  - 디폴트: "+N분" (시간 빚, P6 매출 환산 OFF default)
  - opt-in: "₩N" (매출 환산 모드)
  - 같은 typographic 처리 (IBM Plex Mono 64-80sp), 단위만 다름
- **Border radius scale**:

| 토큰 | px | 사용 |
|---|---|---|
| `sm` | 4 | input·tag |
| `md` | 8 | button·card |
| `lg` | 12 | sheet·modal |
| `phone` | 32 | phone mockup frame only |

- **bubble radius (`9999px`) 금지** — 카테고리 AI 슬롭 패턴

## Motion

- **Approach**: minimal-functional. Quiet.
- **Easing**: 
  - enter: `cubic-bezier(0, 0, 0.2, 1)` (ease-out)
  - exit: `cubic-bezier(0.4, 0, 1, 1)` (ease-in)
  - move: `cubic-bezier(0.4, 0, 0.2, 1)` (ease-in-out)
- **Duration**:
  - micro (state changes): 100-150ms
  - short (fade·slide): 200-300ms
  - medium (sheet·page): 300-400ms
  - long (large transition): 400-500ms — rare
- **Spring·bounce 금지**. Material 3 Expressive default spring도 disable.
- **Celebration animation 금지** — session 완료, 목표 달성에 confetti·glow·grow 모두 X. 대신 단 1줄 한글 fade-in (예: "오늘은 SNS를 2시간 27분 안 봤어요.")
- **Loading**: subtle shimmer 또는 한 줄 dot pulse. 회전 spinner 가능하지만 작게.

## Components

### Buttons

- **Primary (filled)**: 배경 `--text-primary` (black-ish), 텍스트 `--bg`. 12px vertical padding, 20px horizontal. radius `md`. 매우 드물게 사용 (한 화면에 1개 max).
- **Secondary (outlined)**: 배경 `--surface`, 보더 `--divider`, 텍스트 `--text-primary`.
- **Text only**: 색 `--accent` (clay), 배경 없음. 가장 자주 사용되는 CTA.
- **Filled gradient 금지** — AI 슬롭 패턴.

### Inputs

- 배경 `--bg`, 보더 `--divider`, focus 시 `--accent`
- 12px vertical padding, 14px horizontal, radius `md`
- Label은 위쪽에 `--text-secondary` 13sp

### Cards

- 배경 `--surface`, 보더 `--divider` 1px, radius `md` 또는 `lg`
- Shadow 거의 사용 안 함 — divider로 분리. 사용 시 `0 4px 24px rgba(26,26,26,0.04)` 매우 약하게.

### Mobile-specific

- Bottom sheet 적극 사용 (Material 3 default)
- Tab bar: 4탭 max, 텍스트 only (icon 금지 또는 매우 추상적 icon)
- Navigation drawer 회피 — bottom sheet이 모든 secondary action 담당

## Deliberate Departures (Risks)

이 4개가 카테고리에서 kkeugi의 visual signature를 만듭니다.

1. **Hero numeral typography identity**: 매 화면 가장 큰 요소는 하나의 숫자. "+47분" 또는 "₩68,250" — 같은 typographic 처리, 단위만 다름. 본인이 카톡에 screenshot 공유했을 때 *공유하고 싶은 그 숫자*가 design system 자체.

2. **Clay accent `#8B5A3C`**: 한국 productivity 카테고리에 비어있는 색. Toss blue / Kakao yellow / 간단 mint / Linear lime — 모두 cool 또는 saturated. Clay는 adult tone, 따뜻하지만 친근한 척하지 않음.

3. **주간 리포트 = 편지**: 일요일 22:00 카드는 한 paragraph 한글 본문 + embedded hero numeral. 차트·gauge·progress bar 없음. 거울 같은 친구 literal 구현.

4. **IBM Plex Mono on hero numeral**: 한국 productivity 모두 Pretendard Bold tnum. Mono를 가장 중요한 데이터에 쓰는 건 unusual — "거울 = 정직" 의 typographic equivalent.

## Implementation Notes (Flutter)

```yaml
# pubspec.yaml dependencies
pretendard: ^1.0.0  # 또는 fonts/ 디렉토리에 bundling
google_fonts: ^6.1.0  # IBM Plex Mono
```

```dart
// ThemeData configuration sketch
theme: ThemeData(
  scaffoldBackgroundColor: const Color(0xFFFAFAF7),
  colorScheme: const ColorScheme.light(
    primary: Color(0xFF1A1A1A),
    secondary: Color(0xFF8B5A3C),  // clay accent
    surface: Color(0xFFFFFFFF),
    onSurface: Color(0xFF1A1A1A),
    outline: Color(0xFFE8E5DE),
  ),
  textTheme: TextTheme(
    displayLarge: TextStyle(
      fontFamily: 'Pretendard',
      fontWeight: FontWeight.w700,
      fontSize: 56,
      letterSpacing: -1.68,  // -0.03em
      height: 1.0,
    ),
    headlineMedium: TextStyle(
      fontFamily: 'Pretendard',
      fontWeight: FontWeight.w600,
      fontSize: 28,
      letterSpacing: -0.56,
    ),
    bodyLarge: TextStyle(
      fontFamily: 'Pretendard',
      fontWeight: FontWeight.w400,
      fontSize: 16,
      height: 1.6,
    ),
  ),
)

// Hero numeral widget — special case
Text(
  '+47',
  style: GoogleFonts.ibmPlexMono(
    fontWeight: FontWeight.w600,
    fontSize: 72,
    letterSpacing: -2.88,  // -0.04em
    fontFeatures: const [FontFeature.tabularFigures()],
  ),
)
```

## Design System Self-Check Before Shipping

- [ ] hero numeral 하나만 화면당? (multiple = 위계 깨짐)
- [ ] accent color 1번 이하 사용? (2번 이상 = restraint 깨짐)
- [ ] celebration animation 없음? (있으면 비난 X 의 반대 = 압박 ON)
- [ ] purple/violet 0? gradient 0? bubble radius 0?
- [ ] 한글 본문 14sp 이상?
- [ ] 모든 숫자 `tabular-nums`?
- [ ] 카피가 압박 X · 비난 X · 객관 O 톤?

## Information Architecture (2026-05-24 추가, /plan-design-review)

```
첫 진입 (미인증)
  └── 온보딩 5단계
      1. 이유 (관찰 중립 카피, DESIGN.md tone)
      2. PACKAGE_USAGE_STATS 권한 (Android Settings 이동 + 해설)
      3. shock — 어제 사용 시간 (데이터 없으면 fallback: "내일부터 데이터")
      4. 시간당 가치 입력 (skip 가능, ₩30K default)
      5. 채널 선택 (FCM 기본 + 이메일·Telegram 옵션, 1개 이상 필수)

인증 후 (bottom tab 3개)
  ├── 🏠 홈 (today) — hero numeral + 4 카테고리 + 목표 CTA
  ├── 📅 회고 (archive) — 모든 주차 카드 무한 스크롤
  └── ⚙️ 설정
      ├── 시간당 가치 + 매출 환산 toggle
      ├── 작업 시간대 (V1.5 heuristic, 09-18 default)
      ├── 채널 관리 (FCM·이메일·Telegram 토글)
      ├── 목표 설정 (4 카테고리별 threshold)
      ├── 구독 관리 (V1 인앱결제, 2026-05-24 추가)
      │   ├── 현재 plan + 만료일 + 갱신 가능
      │   ├── 결제 내역 (Google Play 링크)
      │   └── 환불 요청 (자체 7일 청약철회)
      ├── 개인정보·권한 (PIPA, 회원탈퇴)
      └── 앱 정보

모달:
  - Paywall (D7 weekly 카드 받은 후 + 매출 환산 toggle 진입 시)
    └── 3 plan 비교 (일회 ₩11K · 월 ₩5.9K · 연 ₩39K) + 7일 무료 체험 CTA
  - 권한 재요청 (PACKAGE_USAGE_STATS 해제 감지 시)
  - 주간 리포트 카드 viewer (FCM tap → 모달)
  - threshold 도달 알람 (로컬 notification tap → 모달)

모달:
  - 권한 재요청 (PACKAGE_USAGE_STATS 해제 감지 시)
  - 주간 리포트 카드 viewer (FCM tap → 모달)
  - threshold 도달 알람 (로컬 notification tap → 모달)
```

## Interaction States (2026-05-24 추가)

| 화면 | LOADING | EMPTY | ERROR | SUCCESS | PARTIAL |
|---|---|---|---|---|---|
| 홈 | "사용 데이터 분석 중" shimmer | "오늘 데이터가 모이는 중. 내일부터 통계가 보입니다" + 목표 CTA | 권한 거부: "사용 통계 접근 권한 필요" + 재요청 CTA + 수동 입력 secondary | hero numeral + 4 카테고리 | 일부 카테고리 정상 display |
| 회고 | shimmer cards | "첫 회고가 도착하면 여기에 모입니다" + D-N 카운트 | network: retry | 무한 스크롤 list | 부분 데이터: disclosure |
| 주간 카드 | "회고 카드 생성 중" + dot pulse | (해당 없음) | LLM 실패: "생성 실패. 다시 시도" + retry | 정상 카드 | (해당 없음) |
| 채널 선택 | 즉시 | "선택된 채널 없음" + 1개 이상 선택 권장 | 이메일 인증 실패·Telegram link 실패 | toggle active | 1개 활성 OK |
| Threshold | 즉시 | "목표 미설정" | (해당 없음) | 슬라이더 + 활성 | 일부만 설정 OK |

## Multi-channel Widget Pattern (2026-05-24 추가)

```
ChannelToggleCard:
  배경:     var(--surface)
  border:   var(--divider) 1px solid
  radius:   8px (md)
  padding:  16px (md)
  layout:   horizontal — [icon] [name + description] [toggle]
  
  Icon:     단색 (#1A1A1A), 24x24, 종/봉투/종이비행기
  Name:     Pretendard Medium 16sp
  Desc:     Pretendard Regular 13sp, var(--text-secondary)
  Toggle:   Material 3 Switch + clay accent 활성색
  
  Inactive 상태: opacity 0.6
  Setup 필요 (이메일/Telegram): right side "추가" text-only CTA in clay
```

## Onboarding 채널 선택 (단계 5) UX (2026-05-24 확정)

```
상단:    Pretendard SemiBold 24sp "주간 회고를 어디로 받으시겠어요?"
설명:    Pretendard Regular 14sp "일요일 22:00 카드를 받을 채널을 1개 이상 선택해주세요."

[icon 종] FCM 푸시           [Switch ON, 기본 선택, 비활성화 불가]
          "기본 알림 (앱 내 + 푸시)"
          
[icon 봉투] 이메일             [Switch OFF, 추가 시 인증 메일 발송]
            "선택 — 이메일 주소 인증"
            
[icon 종이비행기] Telegram     [Switch OFF, 추가 시 Bot deep link]
                  "선택 — 1인 워커 인디 친화"

하단:    "다음" primary button (filled #1A1A1A) — 1개 이상 선택 시 활성
         "나중에 설정" — text-only clay accent, 그래도 FCM 강제 ON
```

## Decisions 추가 항목 (2026-05-24)

| 결정 | 값 |
|---|---|
| 네비게이션 | Bottom tab 3개 (홈·회고·설정) |
| Archive scroll | 무한 스크롤 (월별 그룹 X) |
| Onboarding skip | 권한·채널·시간당가치 모두 skip 가능 (gentle nudge) |
| Telegram link | Deep link (QR X) |
| 이메일 활성 | 인증 메일 필수 |
| Threshold cooldown | daily 1회 (last_triggered_date) |
| 회고 카드 export | 1080×1920 (인스타 스토리) |
| Landscape | 차단 — portrait only |
| Tablet | V1 무시, V1.5 검토 |

## Accessibility (2026-05-24 추가)

```
Touch target:        48dp 최소 (Material 3 default)
Color contrast:      
  text-primary on bg = 14.7:1 ✓✓
  text-secondary on bg = 4.8:1 ✓
  accent (clay) on surface = 4.6:1 ✓
TalkBack 라벨:        모든 interactive element semantic label
Dynamic font size:   Android 시스템 1.0-2.0배 지원
Hangul 본문:          14sp 이상 강제
Screen reader 흐름:    bottom tab → 상단 header → main content → CTA
키보드 navigation:    Android 외부 키보드 사용자 위한 focus indicator
```

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-05-22 | Initial design system v1 created | /design-consultation 세션, design doc의 P2 시점별 톤 분리 + memorable thing "거울 같은 친구" 기반 |
| 2026-05-22 | Pretendard + IBM Plex Mono 채택 | 2026 한국 인디 표준 Pretendard + 거울 톤 위한 Mono 숫자 |
| 2026-05-22 | Clay #8B5A3C accent 선택 | 카테고리 내 빈자리. Toss/Kakao/간단/Linear와 차별 |
| 2026-05-22 | Light default, dark v2 격하 | Korean indie productivity 표준 + morning report 시간대 fit |
| 2026-05-22 | Hero numeral typography identity (₩ / +분) | wedge #1 (시간 빚·매출 환산)을 typography로 직접 표현 |
| 2026-05-22 | Celebration animation 0 | memorable thing "비난 X" + "압박 X" 동시 만족 → "객관" 중립 톤 |
| 2026-05-24 | **V1 = 무료 도구 pivot 반영**: 카톡 channel V2 격하. multi-channel retention (FCM·이메일·Telegram) 도입. 시점별 톤 분리는 channel별로 확장: FCM 관찰 중립 (즉시 알람), 이메일·Telegram 시간 빚 (주간 회고), V2 카톡 관찰 중립 | 본인 회사 겸업 금지 → 사업자 미보유 → 카톡 V2 격하. 새 wedge #3 = multi-channel 다양성 = 1인 워커 친화. |
| 2026-05-24 | **/plan-design-review 완료**: IA tree 8개 화면, interaction state matrix, multi-channel widget pattern, 온보딩 채널 선택 UX (FCM 강제 + 이메일·Telegram 옵션, 1개+), accessibility 섹션, 9개 micro decision. 디자인 score 6.5/10 → 9/10. | W2-W3 빌드 시 implementation 헷갈림 회피. 5화면 wireframe Figma 작성의 spec base. |
| 2026-05-24 | **V1 인앱결제 paid re-pivot 반영**: Paywall modal UX 추가 (D7 weekly 후 + 매출 환산 toggle 진입 시 trigger). 3 plan 비교 UI (일회 ₩11K / 월 ₩5.9K / 연 ₩39K) + 7일 무료 체험 CTA. 구독 관리 화면 추가 (설정 내). 환불 요청 UX (자체 7일 청약철회). | V1 paid product 결정. Google Play Billing 표준 follow. memorable thing "압박 X" 일관 — paywall 톤도 "다음 주부터 더 보시려면" gentle 강조. |
| 2026-05-24 | **Auth Google Sign-In primary 변경**: 온보딩 첫 화면 "카카오로 시작" → "Google로 시작" (Pretendard SemiBold 16sp + Google 로고 left). V2 카톡 연동 시점에 설정 → "카톡 알림 받기" CTA → phone 입력 step. | Android 표준 + Google Play Billing 통합 + W2 일정 단축 + Kakao 비즈 심사 회피. |

## Open Questions

- **Brand naming 한국어**: "끊기" 유지 vs "끊기 (Focus Accountant)" 병기 vs 다른 한국어 이름. 랜딩·X 게시·카톡 채널명 결정 필요. → 마케팅 단계에서 결정.
- **다크 모드 timing**: Phase 1 매출 ₩200만/월 이후 v2 진입. 그 전에 베타 50명이 다크 요구하면 재검토.
- **Material 3 Expressive 적용 여부**: spring motion·shape variety. 현 시점 일부만 채택 (spring motion X, shape variety O).

## References

- [Pretendard GitHub](https://github.com/orioncactus/pretendard)
- [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono)
- [Toss Product Sans 케이스](https://en.sandoll.co.kr/Story/?bmode=view&idx=19492476)
- [Linear Brand Guidelines](https://linear.app/brand)
- [Opal Brand Kit](https://brandkit.opal.so/)
- HTML preview: `/tmp/kkeugi-design-preview.html`

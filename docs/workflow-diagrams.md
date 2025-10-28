# RF S-parameter Analysis Workflow Diagrams

업무 보고서용 Mermaid 다이어그램 - 여러 스타일 제공

---

## 📊 Option 1: Simple Linear Flow (가장 심플)

```mermaid
graph LR
    A[📡 Network Analyzer<br/>SnP Files] --> B[🔄 S-Para Converter<br/>SnP → CSV]
    B --> C[📊 S-Para Hub<br/>Interactive Charts]

    style A fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style B fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style C fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

**설명**: 가장 간단한 3단계 플로우

---

## 📊 Option 2: Vertical Flow with Details (세부 정보 포함)

```mermaid
graph TD
    A[📡 Network Analyzer] -->|S-parameter<br/>Measurement| B[SnP Files<br/>.s1p ~ .s12p]
    B -->|Upload| C[🔄 S-Para Converter]
    C -->|Frequency<br/>Filtering| D[CSV File<br/>Rx Gain Data]
    D -->|Import| E[📊 S-Para Hub<br/>]
    E -->|Plotly.js| F[Interactive<br/>Charts]

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style C fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style D fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    style E fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style F fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
```

**설명**: 세부 단계와 파일 형식 표시

---

## 📊 Option 3: System Architecture (시스템 구조도)

```mermaid
graph TB
    subgraph Measurement["🔬 Measurement Phase"]
        NA[Network Analyzer]
        SNP[SnP Files<br/>S-parameter Data]
    end

    subgraph Conversion["⚙️ Conversion Phase"]
        RFC[S-Para Converter<br/>PyQt6 Desktop App]
        CSV[CSV Output<br/>Rx Gain / Tx Power]
    end

    subgraph Analysis["📈 Analysis Phase"]
        DWS[S-Para Hub ]
        CHART[Plotly Interactive Charts]
    end

    NA --> SNP
    SNP --> RFC
    RFC -->|3GPP Band<br/>Filtering| CSV
    CSV --> DWS
    DWS --> CHART

    style Measurement fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style Conversion fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    style Analysis fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px

    style NA fill:#bbdefb,stroke:#1565c0
    style SNP fill:#90caf9,stroke:#1565c0
    style RFC fill:#ffe0b2,stroke:#ef6c00
    style CSV fill:#ffcc80,stroke:#ef6c00
    style DWS fill:#c8e6c9,stroke:#2e7d32
    style CHART fill:#a5d6a7,stroke:#2e7d32
```

**설명**: 3개 페이즈로 구분된 시스템 구조

---

## 📊 Option 4: Timeline Flow (타임라인 스타일)

```mermaid
timeline
    title RF S-parameter Analysis Workflow
    section Measurement
        Network Analyzer : SnP File Generation
                         : .s1p ~ .s12p formats
    section Conversion
        S-Para Converter : Desktop Application
                     : Frequency Filtering
                     : CSV Export
    section Visualization
        S-Para Hub : Data Import
                   : Interactive Charts
                   : Analysis & Export
```

**설명**: 타임라인 형식 (Mermaid 최신 기능)

---

## 📊 Option 5: Detailed Sequence (상세 시퀀스)

```mermaid
sequenceDiagram
    actor User
    participant NA as 📡 Network<br/>Analyzer
    participant RFC as 🔄 S-Para<br/>Converter
    participant DWS as 📊 S-Para Hub

    User->>NA: Measure S-parameters
    NA-->>User: SnP Files

    User->>RFC: Upload SnP Files
    RFC->>RFC: Parse & Filter<br/>(3GPP Bands)
    RFC-->>User: CSV File (Raptor Style)

    User->>DWS: Import CSV
    DWS->>DWS: Generate Charts
    DWS-->>User: Interactive Graphs

    Note over User,DWS: Complete RF Analysis Workflow
```

**설명**: 사용자 인터랙션 중심 시퀀스 다이어그램

---

## 📊 Option 6: Data Flow (데이터 흐름 중심)

```mermaid
flowchart LR
    subgraph Input["📥 Input Data"]
        SNP[SnP Files<br/>S21, S12, S11, S22]
    end

    subgraph Processing["⚙️ Processing"]
        PARSE[Parse SnP]
        FILTER[Frequency Filter<br/>3GPP Bands]
        CALC[Calculate Metrics<br/>Gain, RL, Isolation]
    end

    subgraph Output["📤 Output"]
        CSV[CSV File<br/>Rx/Tx Data]
        CHART[Interactive Charts<br/> PDF / PPT]
    end

    SNP --> PARSE
    PARSE --> FILTER
    FILTER --> CALC
    CALC --> CSV
    CSV --> CHART

    style Input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Processing fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Output fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

**설명**: 데이터 변환 과정 강조

---

## 📊 Option 7: Feature Highlights (기능 강조)

```mermaid
graph TB
    A[📡 Network Analyzer<br/>SnP Measurement] --> B{🔄 S-Para Converter}

    B --> B1[3GPP Band Filter]
    B --> B3[CSV Export<br/>Raptor Format]

    B1 & B3 --> C[💾 CSV File]

    C --> D[📊 S-Para Hub ]

    D --> D1[Grid Layout<br/>Multi-Band View]
    D --> D2[Interactive Charts]
    D --> D3[PDF Export<br/>Full Report]

    D1 & D2 & D3 --> E[📈 Analysis Results]

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    style C fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    style D fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style E fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px

    style B1 fill:#ffe0b2,stroke:#ef6c00
    style B2 fill:#ffe0b2,stroke:#ef6c00
    style B3 fill:#ffe0b2,stroke:#ef6c00
    style D1 fill:#c8e6c9,stroke:#2e7d32
    style D2 fill:#c8e6c9,stroke:#2e7d32
    style D3 fill:#c8e6c9,stroke:#2e7d32
```

**설명**: 주요 기능 하이라이트

---

## 📊 Option 8: Executive Summary (경영진용 - 가장 심플)

```mermaid
graph LR
    A["📡<br/>Measure"] --> B["⚙️<br/>Convert"] --> C["📊<br/>Analyze"]

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:3px,font-size:16px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:3px,font-size:16px
    style C fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px,font-size:16px
```

**한 줄 설명**:
- **Measure**: Network Analyzer로 S-parameter 측정
- **Convert**: S-Para Converter로 CSV 변환 (주파수 필터링)
- **Analyze**: S-Para Hub에서 그래프 생성 및 분석

---

## 📊 Option 9: PPT-Ready Diagram (PPT 최적화)

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'18px'}}}%%
graph TD
    A["🔬 MEASUREMENT<br/><br/>Network Analyzer<br/>S-parameter Data"]
    B["⚙️ CONVERSION<br/><br/>S-Para Converter<br/>Desktop Application"]
    C["📊 VISUALIZATION<br/><br/>S-Para Hub <br/>Interactive Analysis"]

    A -->|"SnP Files<br/>.s1p ~ .s12p"| B
    B -->|"CSV File<br/>3GPP Filtered"| C

    style A fill:#1976d2,stroke:#0d47a1,stroke-width:3px,color:#fff
    style B fill:#f57c00,stroke:#e65100,stroke-width:3px,color:#fff
    style C fill:#388e3c,stroke:#1b5e20,stroke-width:3px,color:#fff
```

**설명**: 큰 폰트, 강렬한 색상 (PPT 투영에 최적)

---

## 🎯 추천 다이어그램

### 1️⃣ **일반 보고서용**: Option 3 (System Architecture)
- 3개 페이즈 명확히 구분
- 전문적이고 체계적
- 기술 세부사항 포함

### 2️⃣ **경영진 보고용**: Option 8 (Executive Summary)
- 가장 심플
- 핵심만 전달
- 한눈에 이해 가능

### 3️⃣ **PPT 프레젠테이션용**: Option 9 (PPT-Ready)
- 큰 폰트, 강렬한 색상
- 프로젝터 투영에 최적
- 임팩트 있는 디자인

---

## 📝 사용 방법

### Markdown 지원 플랫폼
1. GitHub README.md
2. GitLab
3. Notion
4. Obsidian
5. VS Code (Markdown Preview Enhanced)

### PPT 변환
1. **온라인 렌더링**: https://mermaid.live/
2. **VS Code 확장**: Markdown Preview Mermaid Support
3. **스크린샷**: 렌더링 후 이미지로 저장 → PPT 삽입

### 색상 커스터마이징
```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'primaryColor':'#your-color',
  'primaryTextColor':'#fff',
  'fontSize':'16px'
}}}%%
```

---

---

## 📊 Option 10: Data Verification Purpose (데이터 검증 목적)

```mermaid
graph TB
    subgraph OurData["🔬 Our Measurement Data"]
        NA[Network Analyzer]
        CONV[S-Para Converter]
        OUR[Our CSV Data<br/>Raptor Format]
    end

    subgraph ClientData["🏢 Client Data"]
        CLIENT[Client CSV Data<br/>Proprietary Format]
    end

    subgraph Comparison["⚖️ Comparison & Verification"]
        HUB[S-Para Hub<br/>Django Web Service]
        COMPARE[Side-by-Side<br/>Comparison]
        VERIFY[Data Verification<br/>Result]
    end

    NA --> CONV
    CONV --> OUR
    OUR --> HUB
    CLIENT --> HUB
    HUB --> COMPARE
    COMPARE --> VERIFY

    style OurData fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style ClientData fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    style Comparison fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px

    style NA fill:#bbdefb,stroke:#1565c0
    style CONV fill:#90caf9,stroke:#1565c0
    style OUR fill:#64b5f6,stroke:#1565c0
    style CLIENT fill:#ffcc80,stroke:#ef6c00
    style HUB fill:#a5d6a7,stroke:#2e7d32
    style COMPARE fill:#81c784,stroke:#2e7d32
    style VERIFY fill:#66bb6a,stroke:#2e7d32
```

**설명**: 자사 데이터 vs 고객사 데이터 비교 검증 프로세스

---

## 📊 Option 11: Verification Goal (심플 버전)

```mermaid
graph LR
    A["🔬<br/>Our Data<br/><br/>S-Para Converter"] --> C["⚖️<br/>Comparison<br/><br/>S-Para Hub"]
    B["🏢<br/>Client Data<br/><br/>Proprietary Format"] --> C
    C --> D["✅<br/>Verification<br/><br/>Match/Mismatch"]

    style A fill:#1976d2,stroke:#0d47a1,stroke-width:3px,color:#fff
    style B fill:#f57c00,stroke:#e65100,stroke-width:3px,color:#fff
    style C fill:#388e3c,stroke:#1b5e20,stroke-width:3px,color:#fff
    style D fill:#689f38,stroke:#33691e,stroke-width:3px,color:#fff
```

**설명**: 가장 심플한 비교 검증 플로우 (경영진용)

---

## 📊 Option 12: Detailed Verification Flow (상세 검증 플로우)

```mermaid
graph TD
    A[📡 Network Analyzer<br/>S-parameter Measurement] --> B[🔄 S-Para Converter]
    B --> C[💾 Our CSV Data<br/>Raptor Format]

    CLIENT[🏢 Client Provided<br/>CSV Data]

    C --> HUB[📊 S-Para Hub<br/>Django Web Service]
    CLIENT --> HUB

    HUB --> LOAD[Load Both Datasets]
    LOAD --> ALIGN[Frequency Alignment<br/>Band Matching]
    ALIGN --> VIS[Visual Comparison<br/>Overlay Charts]
    VIS --> CALC[Calculate Difference<br/>Δ Gain, Δ RL]
    CALC --> RESULT{Verification<br/>Result}

    RESULT -->|"Match<br/>(Δ < 0.5dB)"| PASS[✅ Verified<br/>Data Consistent]
    RESULT -->|"Mismatch<br/>(Δ > 0.5dB)"| FAIL[⚠️ Review Required<br/>Investigate Difference]

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style C fill:#90caf9,stroke:#1565c0,stroke-width:2px
    style CLIENT fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px
    style HUB fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style LOAD fill:#a5d6a7,stroke:#2e7d32
    style ALIGN fill:#a5d6a7,stroke:#2e7d32
    style VIS fill:#a5d6a7,stroke:#2e7d32
    style CALC fill:#a5d6a7,stroke:#2e7d32
    style RESULT fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style PASS fill:#81c784,stroke:#2e7d32,stroke-width:2px
    style FAIL fill:#ffb74d,stroke:#ef6c00,stroke-width:2px
```

**설명**: 검증 프로세스 전체 흐름 (Pass/Fail 조건 포함)

---

## 📊 Option 13: Comparison Features (기능 중심)

```mermaid
graph TB
    subgraph Input["📥 Input Sources"]
        OUR[Our Measurement<br/>S-Para Converter]
        CLIENT[Client Data<br/>Various Formats]
    end

    subgraph Tool["🛠️ S-Para Hub Features"]
        IMPORT[Multi-Format Import]
        NORM[Data Normalization]
        OVERLAY[Overlay Visualization]
        DIFF[Difference Calculation]
        REPORT[Verification Report]
    end

    subgraph Output["📤 Verification Output"]
        VISUAL[Visual Comparison<br/>Side-by-Side Charts]
        METRIC[Numerical Metrics<br/>Δ Gain, Δ RL, Δ Isolation]
        CONCLUSION[Pass/Fail<br/>Conclusion]
    end

    OUR & CLIENT --> IMPORT
    IMPORT --> NORM
    NORM --> OVERLAY
    OVERLAY --> DIFF
    DIFF --> REPORT
    REPORT --> VISUAL
    REPORT --> METRIC
    REPORT --> CONCLUSION

    style Input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Tool fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Output fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

**설명**: S-Para Hub의 비교 검증 기능 강조

---

## 📊 Option 14: Use Case Diagram (사용 시나리오)

```mermaid
graph LR
    A["📋 Use Case<br/><br/>PA Module<br/>Acceptance Test"] --> B["📊 Tool Purpose<br/><br/>Compare Our Data<br/>vs Client Spec"]

    B --> C1["✅ Scenario 1<br/>Data Match<br/>→ Ship Product"]
    B --> C2["⚠️ Scenario 2<br/>Data Mismatch<br/>→ Root Cause Analysis"]

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    style C1 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style C2 fill:#ffccbc,stroke:#d84315,stroke-width:2px
```

**설명**: 실제 사용 사례 중심

---

## 📊 Option 15: PPT Executive Version (경영진 보고용)

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'20px'}}}%%
graph TD
    A["🎯 TOOL PURPOSE<br/><br/>Data Verification Tool<br/>for Client Acceptance"]

    A --> B["📊 FUNCTION<br/><br/>Compare Our Measurement<br/>vs Client Specification"]

    B --> C["✅ GOAL<br/><br/>Ensure Data Consistency<br/>Before Product Delivery"]

    style A fill:#1976d2,stroke:#0d47a1,stroke-width:4px,color:#fff
    style B fill:#f57c00,stroke:#e65100,stroke-width:4px,color:#fff
    style C fill:#388e3c,stroke:#1b5e20,stroke-width:4px,color:#fff
```

**설명**: 경영진용 - 큰 폰트, 핵심만

---

## 📊 Option 16: Before/After Comparison (문제 해결 강조)

```mermaid
graph TB
    subgraph Before["❌ Before (Manual Process)"]
        B1[Export Excel<br/>from each tool]
        B2[Manual alignment<br/>in spreadsheet]
        B3[Visual inspection<br/>Human error prone]
        B4[Time: 2-3 hours<br/>per dataset]

        B1 --> B2 --> B3 --> B4
    end

    subgraph After["✅ After (S-Para Hub)"]
        A1[Auto import<br/>both datasets]
        A2[Auto alignment<br/>by frequency]
        A3[Side-by-side charts<br/>Difference overlay]
        A4[Time: 5 minutes<br/>Automated report]

        A1 --> A2 --> A3 --> A4
    end

    Before -.->|"S-Para Hub<br/>Solution"| After

    style Before fill:#ffebee,stroke:#c62828,stroke-width:2px
    style After fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

**설명**: 기존 방식 vs 새로운 방식 비교 (ROI 강조)

---

## 📊 Option 17: Data Flow with Verification (통합 플로우)

```mermaid
graph TB
    A[📡 Network Analyzer] -->|SnP| B[🔄 S-Para Converter]
    B -->|CSV| C[(Our Database)]

    CLIENT[🏢 Client] -->|CSV/Excel| D[(Client Database)]

    C & D --> E[📊 S-Para Hub<br/>Comparison Engine]

    E --> F{Difference<br/>Analysis}

    F -->|"Δ < 0.5dB"| G[✅ PASS<br/>Ship to Client]
    F -->|"Δ > 0.5dB"| H[⚠️ INVESTIGATE<br/>Root Cause]

    H --> I[Debug Mode<br/>Detailed Analysis]
    I --> J[Corrective Action]
    J --> E

    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style C fill:#90caf9,stroke:#1565c0,stroke-width:2px
    style CLIENT fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px
    style D fill:#ffcc80,stroke:#ef6c00,stroke-width:2px
    style E fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style F fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style G fill:#81c784,stroke:#2e7d32,stroke-width:3px
    style H fill:#ffb74d,stroke:#ef6c00,stroke-width:2px
    style I fill:#ffccbc,stroke:#d84315
    style J fill:#ffab91,stroke:#d84315
```

**설명**: 검증 실패 시 재측정 루프 포함

---

## 🎯 상황별 추천 (비교 검증용)

| 보고 대상 | 추천 다이어그램 | 특징 |
|----------|---------------|------|
| **경영진** | Option 15 | 초심플, 핵심만, 큰 폰트 |
| **고객사** | Option 10 | 전문적, 양측 데이터 명확 |
| **기술팀** | Option 12 | 상세 프로세스, Pass/Fail 조건 |
| **영업팀** | Option 16 | Before/After ROI 강조 |
| **품질팀** | Option 17 | 재측정 루프, 품질 관리 |

---

**파일 위치**: `docs/workflow-diagrams.md`
**생성일**: 2025-10-27
**업데이트**: 2025-10-27 (비교 검증 다이어그램 추가)
**용도**: 업무 보고서, PPT 프레젠테이션, 기술 문서, 고객 제안서

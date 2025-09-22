/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { GoogleGenAI, Chat } from "@google/genai";

// Declare Lucide on the window object for global access
declare global {
    interface Window {
        lucide: {
            createIcons: (options?: any) => void;
        };
    }
}


document.addEventListener("DOMContentLoaded", () => {

    // --- Feature Flags ---
    const featureFlags: { [key:string]: boolean } = {
        pioneersSection: true,
        chatbot: true,
    };

    const isFeatureEnabled = (flagName: string): boolean => {
        const override = localStorage.getItem(`ff_${flagName}`);
        if (override !== null) {
            return override === 'true';
        }
        return featureFlags[flagName] ?? false;
    };

    const applyFeatureFlags = () => {
        document.querySelectorAll<HTMLElement>('[data-feature-flag]').forEach(element => {
            const flagName = element.dataset.featureFlag;
            if (flagName && !isFeatureEnabled(flagName)) {
                element.style.display = 'none';
                if (element.tagName === 'SECTION' && element.id) {
                    const navLink = document.querySelector(`.sidebar-nav a[href="#${element.id}"]`);
                    if (navLink && navLink.parentElement) {
                        navLink.parentElement.style.display = 'none';
                    }
                }
            }
        });
    };
    

    // --- Gemini Chatbot ---
    let chat: Chat | null = null;
    const ai = new GoogleGenAI({apiKey: process.env.API_KEY});

    const initializeChat = () => {
        const systemInstruction = `You are an expert assistant for Voither. Your tone is professional, visionary, and precise. Your main goal is to explain Voither's paradigm-shifting approach to potential investors and partners.

        **Core Thesis: A New Architecture for Healthcare**
        Voither is pioneering a new fundamental architecture for healthcare that solves two core problems: the **Cloud Automation Barrier** (cloud latency prevents real-time automation) and the **Data Privacy Crisis** (sensitive data is vulnerable in the cloud).

        **The Solution (Problem -> Solution Mapping):**
        - **Problem: The Cloud Automation Barrier.** Cloud latency and privacy risks prevent real-time automation.
        - **Solution: Voither Private Edge Cloud.** An on-site mesh of Apple Silicon nodes that brings AI processing to the data, eliminating these barriers.
        - **Problem: Insecure, Generic Systems.** Standard OSs aren't built for mission-critical, real-time healthcare AI.
        - **Solution: HealthOS.** A secure, purpose-built operating system optimized for the Mestral Engine's autonomous tasks.
        - **Problem: Anachronistic, Manual Workflows.** Healthcare runs on inefficient processes that cause burnout and errors.
        - **Solution: Mestral Engine.** A powerful, locally-run LLM that automates complex clinical workflows in real-time.
        - **Problem: Lack of integrated public health tools.** Critical public health workflows are fragmented.
        - **Solution: Sortio Platform.** Voither's flagship public health platform that uses the full stack to automate workflows like triage and bed regulation.

        **The Architecture (The Turnkey Advantage):**
        Voither delivers a complete, managed, all-in-one solution. This is our business model and how we guarantee results.
        - **Strategic Hardware (Apple Silicon):** We use **Mac Studio M3 Ultra nodes** for their unmatched power efficiency and local compute power.
        - **Strategic Connectivity (Starlink):** A 'satellite-first' approach with **Starlink** creates a resilient mesh network independent of terrestrial fiber.
        - **The All-in-One Guarantee:** By managing everything, we deliver unmatched **resilience, economy, and security**. This vertical integration is the foundation of our **Privacy by Design** promise: sensitive patient data (PHI) is processed on-site and *never* leaves the local premises.

        **Key Principles:**
        - **Privacy by Design (Non-Negotiable):** This is the core of our architecture. All PHI is processed locally within the encrypted HealthOS environment.
        - **Interactive Architecture Diagram:** The "Architecture" section has an interactive diagram. Encourage users to click on the different layers (Voither Cloud, HealthOS, Mestral Engine) to understand how they work together.
        - **Rhizome/Mesh Architecture:** A decentralized web of autonomous 'cells' (hospitals, clinics). A failure in one node does NOT compromise the entire network.

        **Key Information & Corrections:**
        - **Impact Metrics are Projections:** When asked about metrics (e.g., 85% TCO reduction), clarify that these are **projections and targets** based on our model, as we are in a pre-market phase.
        - **It's NOT just for bad internet:** Our network is a strategic choice for **autonomy, resilience, and performance**.
        - **It's NOT about latency:** Latency is the *symptom*. The real problem is the architectural dependency on the cloud. We solve the foundational problem, enabling true automation with inherent privacy.`;
        
        chat = ai.chats.create({
            model: 'gemini-2.5-flash',
            config: {
                systemInstruction: systemInstruction,
            },
        });
    };
    
    // FIX: Moved addMessage to a higher scope to be accessible by the language switcher event listener.
    // This resolves the "Cannot find name 'addMessage'" error.
    const addMessage = (content: string, type: 'user' | 'bot') => {
        const messagesContainer = document.getElementById('chatbot-messages');
        if (!messagesContainer) return;

        const messageWrapper = document.createElement('div');
        messageWrapper.className = `chat-message ${type}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = content; // Using innerHTML to support basic formatting like <strong>
        
        messageWrapper.appendChild(messageContent);
        messagesContainer.appendChild(messageWrapper);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // --- Smooth Scroll Polyfill for older browsers ---
    if (!('scrollBehavior' in document.documentElement.style)) {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (this: HTMLAnchorElement, e: MouseEvent) {
                const hrefAttr = this.getAttribute('href');
                if (!hrefAttr || hrefAttr.length <= 1) return;
                const targetElement = document.querySelector(hrefAttr);
                if (targetElement) {
                    e.preventDefault();
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                    window.scrollTo({ top: targetPosition, behavior: 'smooth' }); // Simplified polyfill
                }
            });
        });
    }

    // --- Translations and Language Switcher ---
    const translations: { [key: string]: { [key: string]: string } } = {
        en: {
            pageTitle: "Voither | The End of Manual Workflows in Healthcare",
            proudlyPartOf: "Proudly member of",
            msForStartups: "Microsoft for Startups",
            cfForStartups: "Cloudflare for Startups",
            
            heroTitleNew: "Autonomous Healthcare.",
            heroPitchNew: "Voither delivers the new foundation for healthcare: an on-site AI platform that automates workflows with absolute privacy and resilience. The end of manual work is here.",
            heroCtaPrimary: "Explore The Solution",
            heroCtaSecondary: "Become a Partner",
            
            navSolution: "The Solution",
            navArchitecture: "The Architecture",
            navImpact: "The Impact",
            navApplication: "In Action",
            navResearch: "Foundations",
            navAbout: "About",
            navContact: "Contact",
            
            complianceTitle: "Compliance",
            complianceLGPD: "LGPD",
            complianceHIPAA: "HIPAA",
            complianceFHIR: "FHIR",
            complianceANVISA: "ANVISA RDC",
            complianceISO13485: "ISO 13485",

            solutionTitle: "From Barrier to Breakthrough",
            solutionSubtitle: "Healthcare's core challenges are architectural. We built the new architecture to solve them.",
            solutionProblem1Title: "The Cloud Automation Barrier",
            solutionProblem1Desc: "Cloud latency prevents real-time AI automation and exposes sensitive data.",
            solutionSolution1Title: "Voither Edge Cloud",
            solutionSolution1Desc: "An on-site mesh of Apple Silicon nodes that brings AI processing to the data, solving latency and privacy risks.",
            solutionProblem2Title: "Insecure, Generic Systems",
            solutionProblem2Desc: "General-purpose OSs lack the security and real-time focus for mission-critical healthcare AI.",
            solutionSolution2Title: "HealthOS",
            solutionSolution2Desc: "A secure, purpose-built OS that guarantees stability for autonomous AI workflows.",
            solutionProblem3Title: "Anachronistic Workflows",
            solutionProblem3Desc: "Manual, fragmented processes lead to burnout, errors, and critical delays in care.",
            solutionSolution3Title: "Mestral Engine",
            solutionSolution3Desc: "A powerful, locally-run LLM that automates complex clinical workflows in real-time.",
            
            architectureTitle: "A Turnkey Platform for Healthcare",
            architectureSubtitle: "We deliver a complete, vertically-integrated solution—from silicon to application—to guarantee results.",
            architecturePillar1Title: "Strategic Hardware: Apple Silicon",
            architecturePillar1Desc: "Powered by **Mac Studio M3 Ultra nodes**, our managed hardware guarantees the local performance and efficiency required for real-time AI.",
            architecturePillar2Title: "Resilient Connectivity: Starlink",
            architecturePillar2Desc: "A 'satellite-first' approach with **Starlink** creates a high-availability mesh network independent of terrestrial fiber for radical resilience.",
            architecturePillar3Title: "The All-in-One Advantage",
            architecturePillar3Desc: "Our managed model ensures unmatched resilience, economy, and security, delivering absolute **Privacy by Design**.",

            techDeepDiveTitle: "Technology Deep Dive",
            techDeepDiveSubtitle: "Our architecture is a vertically integrated stack where each layer is purpose-built for the next. Click any component to learn more.",
            
            stackVoitherTitle: "Voither Edge Cloud",
            stackHealthOSTitle: "HealthOS",
            stackMestralTitle: "Mestral Engine",
            mestralPIRTitle: "PIR: Workflow Blueprint",
            mestralROETitle: "ROE: The Conductor",
            mestralRMSTitle: "RMS: Perfect Memory",
            mestralRRETitle: "RRE: Reasoning Core",
            mestralMDLTitle: "MDL: Intelligent Archivist",
            mestralPIRDesc: "Translates complex clinical guidelines into structured, executable code, turning static PDFs into automated actions.",
            mestralROEDesc: "The state machine that executes the PIR blueprint, orchestrating tasks and making the 'Next Best Action' decision.",
            mestralRMSDesc: "An immutable log of every action and state change, ensuring 100% traceability and auditability.",
            mestralRREDesc: "The semantic layer that 'understands' clinical context, allowing the system to make intelligent, data-driven decisions.",
            mestralMDLDesc: "Uses semantic compression to efficiently store event data without losing critical information, vital for long-term edge storage.",
            modalVoitherCloudDesc: "This is the foundational layer: a private, on-premise mesh network of high-performance Apple Silicon nodes (Mac Studio M3 Ultra). By bringing the infrastructure to the data, we eliminate cloud latency and ensure sensitive patient information never leaves the secure local network.",
            modalHealthOSDesc: "HealthOS is the secure, real-time operating system running on Voither hardware. Unlike general-purpose OSs, HealthOS is hardened and optimized for the Mestral Engine's mission-critical tasks, guaranteeing the low latency required for autonomous AI.",
            modalMestralEngineDesc: "The Mestral Engine is the AI brain of the system, running locally within HealthOS. It is a suite of specialized models that work together to understand, orchestrate, and automate complex clinical processes in real-time, directly at the point of care.",

            impactTitle: "The Projected Impact of True Automation",
            impactSubtitle: "By automating broken workflows, our platform is designed to deliver transformative results.",
            impact1Value: "85%",
            impact1Title: "Projected TCO Reduction",
            impact1Desc: "Up to 85% TCO savings projected with our fully managed, all-in-one model.",
            impact2Value: "<12 mo",
            impact2Title: "Projected ROI",
            impact2Desc: "Our turnkey model is designed to deliver a full return on investment in under 12 months.",
            impact3Value: "40-70%",
            impact3Title: "Target Admin Load Reduction",
            impact3Desc: "Our goal is to reduce the administrative burden on clinicians by 40-70%.",
            impact4Value: "<50ms",
            impact4Title: "Local AI Automation",
            impact4Desc: "Guaranteed low latency to enable real-time workflow automation at the point of care.",
            
            applicationTitle: "Sortio: Automation in Action",
            applicationSubtitle: "Sortio, Voither's public health division, uses the Mestral Engine to automate critical bottlenecks in public health.",
            
            pioneer1Title: "Intelligent Bed Regulation",
            pioneer1Desc: "Local AI automates bed allocation, targeting up to a 50% reduction in patient wait times.",
            pioneer2Title: "Automated NLP Triage",
            pioneer2Desc: "Clinicians use voice commands. The local LLM instantly understands, structures, and acts on the information.",
            pioneer3Title: "Dynamic & Autonomous Queues",
            pioneer3Desc: "Sortio runs a fully automated queueing system that re-prioritizes patients based on live clinical data.",
            pioneer4Title: "Automated Transfer Orchestration",
            pioneer4Desc: "The platform fully automates patient transfers, from request to coordination with emergency services.",

            researchTitle: "Theoretical Foundations",
            researchSubtitle: "Our work is built on established research in distributed systems, semantic modeling, and AI.",
            research1Title: "Rhizomatic Structures in System Design",
            research1Desc: "Using concepts from Deleuze and Guattari to build decentralized, non-hierarchical networks that are inherently fault-tolerant.",
            research2Title: "Offline-First & Local-First Paradigms",
            research2Desc: "Leveraging CRDTs and event sourcing to ensure data consistency and 100% functionality during network outages.",
            research3Title: "Information Theory in Healthcare AI",
            research3Desc: "Applying principles like Minimum Description Length (MDL) for efficient, semantic data compression without information loss.",
            researchLink: "Read More",
            
            aboutSectionTitle: "The Mind Behind Voither",
            founderName: "Dr. Gustavo Mendes",
            founderTitle: "Founder & CEO | CRM/SP 218133",
            founderBio: "Voither was founded by Dr. Gustavo Mendes e Silva, a psychiatrist (FAMEMA) and public administrator (UNESP). His unique journey combines deep clinical experience with a passion for systemic innovation, including work with the UN (UNFPA) and PAHO in Washington D.C., and winning the YouthAgainstAIDS Ahead Hackathon. Before Voither, he managed healthcare networks for São Paulo, witnessing the burdens that distract clinicians from patient care.",
            thesis: `"Healthcare systems are broken because they are manual. We built Voither to automate them from the ground up."`,
            quoteAttribution: "— Dr. Gustavo Mendes e Silva, Founder & CEO, Voither",

            contactTitle: "Become a Foundational Partner",
            contactSubtitle: "We are seeking investors and partners to build the future of public health.",
            formLabelName: "Full Name",
            formPlaceholderName: "Your Name",
            formLabelEmail: "Email Address",
            formPlaceholderEmail: "you@example.com",
            formLabelMessage: "Message",
            formPlaceholderMessage: "Tell us how you'd like to collaborate...",
            formSubmitButton: "Send Message",
            formSuccessTitle: "Thank You!",
            formSuccessMessage: "Your message has been sent. We'll be in touch shortly.",
            
            faqTitle: "Ask Anything",
            faqWelcome: "Have a question? Ask our AI assistant.",
            faqPlaceholder: "Ask about Voither's technology...",
            faqQ1: "What is a 'Private Edge Cloud'?",
            faqA1: "An architecture where AI processing occurs on local hardware. By design, all patient data remains on-site, ensuring maximum privacy and offline functionality. Our cloud layer only handles anonymized metadata.",
            faqQ2: "How do you guarantee operation during internet outages?",
            faqA2: "Our 'Offline-First' design ensures all critical functions run 100% on local hardware. Data syncs automatically when connectivity is restored.",
            faqQ3: "What hardware is required?",
            faqA3: "Our platform uses specific hardware (Mac Studio M3 Ultra nodes). This enables powerful local AI with massive energy savings, fully managed by Voither.",
            faqQ4: "Does Voither replace our existing EHR?",
            faqA4: "No. Voither is a non-disruptive overlay that integrates with and enhances your existing EHR with intelligent automation, requiring no costly migration.",
            faqQ5: "Voither, HealthOS, and Sortio?",
            faqA5: "Voither is the company and our Edge Cloud infrastructure. HealthOS is the secure OS. The Mestral Engine is the AI 'brain'. Sortio is our public health platform that uses the entire stack.",
            faqQ6: "Why is HealthOS a core part of the stack?",
            faqA6: "Standard OSs are not built for mission-critical, real-time AI. HealthOS is purpose-built to guarantee the stability and security for autonomous clinical workflows.",
            faqQ7: "Is this only for places with bad internet?",
            faqA7: "No. It's a strategic choice for any facility prioritizing data privacy, resilience, and the real-time performance needed for true automation. It's about autonomy, not just connectivity.",
            faqQ8: "How does the 'all-in-one' model benefit us?",
            faqA8: "By delivering a fully managed, turnkey solution, we eliminate complexity, reduce your TCO, and guarantee performance, security, and resilience.",
            
            chatbotTitle: "Voither AI Assistant",
            chatbotGreeting: "Hello! How can I help you understand Voither's technology?",
            chatbotPlaceholder: "Ask about our technology...",
            copyright: "&copy; 2025 VOITHER. All rights reserved.",

            cookieConsentText: "We use cookies to enhance your browsing experience and analyze our traffic. By clicking 'Accept', you consent to our use of cookies.",
            cookieAccept: "Accept",
            cookieDecline: "Decline",
        },
        pt: {
            pageTitle: "Voither | O Fim dos Fluxos de Trabalho Manuais na Saúde",
            proudlyPartOf: "Orgulhosamente membro de",
            msForStartups: "Microsoft for Startups",
            cfForStartups: "Cloudflare for Startups",
            
            heroTitleNew: "Saúde Autônoma.",
            heroPitchNew: "A Voither entrega a nova fundação para a saúde: uma plataforma de IA local que automatiza fluxos de trabalho com privacidade e resiliência absolutas. O fim do trabalho manual chegou.",
            heroCtaPrimary: "Explore a Solução",
            heroCtaSecondary: "Seja um Parceiro",
            
            navSolution: "A Solução",
            navArchitecture: "A Arquitetura",
            navImpact: "O Impacto",
            navApplication: "Em Ação",
            navResearch: "Fundações",
            navAbout: "Sobre",
            navContact: "Contato",

            complianceTitle: "Conformidade",
            complianceLGPD: "LGPD",
            complianceHIPAA: "HIPAA",
            complianceFHIR: "FHIR",
            complianceANVISA: "ANVISA RDC",
            complianceISO13485: "ISO 13485",

            solutionTitle: "Da Barreira à Revolução",
            solutionSubtitle: "Os desafios centrais da saúde são arquitetônicos. Nós construímos a nova arquitetura para resolvê-los.",
            solutionProblem1Title: "A Barreira da Automação na Nuvem",
            solutionProblem1Desc: "A latência da nuvem impede a automação com IA em tempo real e expõe dados sensíveis.",
            solutionSolution1Title: "Voither Edge Cloud",
            solutionSolution1Desc: "Uma malha local de nós Apple Silicon que leva o processamento de IA aos dados, resolvendo a latência e os riscos de privacidade.",
            solutionProblem2Title: "Sistemas Genéricos e Inseguros",
            solutionProblem2Desc: "SOs de propósito geral não têm o foco em segurança e tempo real para IA de missão crítica em saúde.",
            solutionSolution2Title: "HealthOS",
            solutionSolution2Desc: "Um SO seguro e construído sob medida que garante a estabilidade para fluxos de trabalho autônomos de IA.",
            solutionProblem3Title: "Fluxos de Trabalho Anacrônicos",
            solutionProblem3Desc: "Processos manuais e fragmentados causam esgotamento, erros e atrasos críticos no cuidado.",
            solutionSolution3Title: "Mestral Engine",
            solutionSolution3Desc: "Um poderoso LLM que roda localmente para automatizar fluxos de trabalho clínicos complexos em tempo real.",
            
            architectureTitle: "Uma Plataforma Turnkey para a Saúde",
            architectureSubtitle: "Entregamos uma solução completa e verticalmente integrada — do silício à aplicação — para garantir resultados.",
            architecturePillar1Title: "Hardware Estratégico: Apple Silicon",
            architecturePillar1Desc: "Potencializada por nós **Mac Studio M3 Ultra**, nosso hardware gerenciado garante a performance e eficiência local para IA em tempo real.",
            architecturePillar2Title: "Conectividade Resiliente: Starlink",
            architecturePillar2Desc: "Uma abordagem 'satélite-primeiro' com a **Starlink** cria uma rede mesh de alta disponibilidade independente de fibra terrestre para resiliência radical.",
            architecturePillar3Title: "A Vantagem 'All-in-One'",
            architecturePillar3Desc: "Nosso modelo gerenciado assegura resiliência, economia e segurança inigualáveis, entregando **Privacidade desde a Concepção**.",

            techDeepDiveTitle: "Mergulho Técnico na Tecnologia",
            techDeepDiveSubtitle: "Nossa arquitetura é uma stack verticalmente integrada onde cada camada é construída para a próxima. Clique em qualquer componente para saber mais.",
            
            stackVoitherTitle: "Voither Edge Cloud",
            stackHealthOSTitle: "HealthOS",
            stackMestralTitle: "Mestral Engine",
            mestralPIRTitle: "PIR: Blueprint do Fluxo",
            mestralROETitle: "ROE: O Maestro",
            mestralRMSTitle: "RMS: Memória Perfeita",
            mestralRRETitle: "RRE: Núcleo de Raciocínio",
            mestralMDLTitle: "MDL: Arquivista Inteligente",
            mestralPIRDesc: "Traduz diretrizes clínicas complexas em código estruturado e executável, transformando PDFs estáticos em ações automatizadas.",
            mestralROEDesc: "A máquina de estados que executa o blueprint do PIR, orquestrando tarefas e tomando a decisão da 'Próxima Melhor Ação'.",
            mestralRMSDesc: "Um registro imutável de cada ação e mudança de estado, garantindo 100% de rastreabilidade e auditabilidade.",
            mestralRREDesc: "A camada semântica que 'entende' o contexto clínico, permitindo que o sistema tome decisões inteligentes baseadas em dados.",
            mestralMDLDesc: "Usa compressão semântica para armazenar dados de eventos de forma eficiente sem perder informação crítica.",
            modalVoitherCloudDesc: "Esta é a camada fundamental: uma rede mesh privada e local de nós de alto desempenho Apple Silicon (Mac Studio M3 Ultra). Ao trazer a infraestrutura para os dados, eliminamos a latência da nuvem e garantimos que informações sensíveis de pacientes nunca saiam da rede local segura.",
            modalHealthOSDesc: "O HealthOS é o sistema operacional seguro e de tempo real que roda no hardware Voither. Diferente de SOs de propósito geral, o HealthOS é reforçado e otimizado para as tarefas de missão crítica do Mestral Engine, garantindo a baixa latência necessária para IA autônoma.",
            modalMestralEngineDesc: "O Mestral Engine é o cérebro de IA do sistema, rodando localmente no HealthOS. É um conjunto de modelos especializados que traballham juntos para orquestrar e automatizar processos clínicos complexos em tempo real, diretamente no ponto de atendimento.",

            impactTitle: "O Impacto Projetado da Verdadeira Automação",
            impactSubtitle: "Ao automatizar fluxos de trabalho quebrados, nossa plataforma é projetada para entregar resultados transformadores.",
            impact1Value: "85%",
            impact1Title: "Redução Projetada de TCO",
            impact1Desc: "Até 85% de economia de TCO projetada com nosso modelo 'all-in-one' totalmente gerenciado.",
            impact2Value: "<12 meses",
            impact2Title: "ROI Projetado",
            impact2Desc: "Nosso modelo turnkey é projetado para entregar um retorno completo do investimento em menos de 12 meses.",
            impact3Value: "40-70%",
            impact3Title: "Redução Alvo na Carga Admin.",
            impact3Desc: "Nosso objetivo é reduzir a carga administrativa dos clínicos em 40-70%.",
            impact4Value: "<50ms",
            impact4Title: "Automação Local com IA",
            impact4Desc: "Baixa latência garantida para permitir automação de fluxos de trabalho em tempo real no ponto de atendimento.",
            
            applicationTitle: "Sortio: Automação em Ação",
            applicationSubtitle: "Sortio, a divisão de saúde pública da Voither, usa o Mestral Engine para automatizar gargalos críticos na saúde pública.",
            
            pioneer1Title: "Regulação Inteligente de Leitos",
            pioneer1Desc: "A IA local automatiza a alocação de leitos, visando uma redução de até 50% nos tempos de espera dos pacientes.",
            pioneer2Title: "Triagem Automatizada com PNL",
            pioneer2Desc: "Clínicos usam comandos de voz. O LLM local entende, estrutura e age instantaneamente sobre a informação.",
            pioneer3Title: "Filas Dinâmicas e Autônomas",
            pioneer3Desc: "O Sortio opera um sistema de filas automatizado que reprioriza pacientes com base em dados clínicos ao vivo.",
            pioneer4Title: "Orquestração de Transferências",
            pioneer4Desc: "A plataforma automatiza totalmente as transferências de pacientes, desde a solicitação até a coordenação com serviços de emergência.",

            researchTitle: "Fundações Teóricas",
            researchSubtitle: "Nosso trabalho se baseia em pesquisas consolidadas em sistemas distribuídos, modelagem semântica e IA.",
            research1Title: "Estruturas Rizomáticas em Design de Sistemas",
            research1Desc: "Usando conceitos de Deleuze e Guattari para construir redes descentralizadas, não hierárquicas e inerentemente tolerantes a falhas.",
            research2Title: "Paradigmas Offline-First e Local-First",
            research2Desc: "Utilizando CRDTs e 'event sourcing' para garantir consistência de dados e 100% de funcionalidade durante quedas de rede.",
            research3Title: "Teoria da Informação em IA na Saúde",
            research3Desc: "Aplicando princípios como MDL (Minimum Description Length) para compressão de dados semântica e eficiente.",
            researchLink: "Leia Mais",
            
            aboutSectionTitle: "A Mente por Trás da Voither",
            founderName: "Dr. Gustavo Mendes",
            founderTitle: "Fundador & CEO | CRM/SP 218133",
            founderBio: "A Voither foi fundada pelo Dr. Gustavo Mendes e Silva, psiquiatra (FAMEMA) e administrador público (UNESP). Sua jornada única combina profunda experiência clínica com uma paixão por inovação sistêmica, incluindo trabalho com a ONU (UNFPA) e OPAS em Washington D.C., e a vitória no hackathon YouthAgainstAIDS Ahead. Antes da Voither, ele gerenciou redes de saúde para São Paulo, testemunhando os fardos que distraem os clínicos do cuidado ao paciente.",
            thesis: `"Os sistemas de saúde estão quebrados porque são manuais. Construímos a Voither para automatizá-los desde o início."`,
            quoteAttribution: "— Dr. Gustavo Mendes e Silva, Fundador & CEO, Voither",

            contactTitle: "Torne-se um Parceiro Fundador",
            contactSubtitle: "Buscamos investidores e parceiros para construir o futuro da saúde pública.",
            formLabelName: "Nome Completo",
            formPlaceholderName: "Seu Nome",
            formLabelEmail: "Endereço de Email",
            formPlaceholderEmail: "voce@exemplo.com",
            formLabelMessage: "Mensagem",
            formPlaceholderMessage: "Conte-nos como gostaria de colaborar...",
            formSubmitButton: "Enviar Mensagem",
            formSuccessTitle: "Obrigado!",
            formSuccessMessage: "Sua mensagem foi enviada. Entraremos em contato em breve.",
            
            faqTitle: "Pergunte Qualquer Coisa",
            faqWelcome: "Tem uma pergunta? Pergunte ao nosso assistente de IA.",
            faqPlaceholder: "Pergunte sobre a tecnologia da Voither...",
            faqQ1: "O que é uma 'Private Edge Cloud'?",
            faqA1: "Uma arquitetura onde o processamento de IA ocorre em hardware local. Por design, todos os dados de pacientes permanecem no local, garantindo máxima privacidade e funcionalidade offline. Nossa nuvem lida apenas com metadados anônimos.",
            faqQ2: "Como garantem a operação durante quedas de internet?",
            faqA2: "Nosso design 'Offline-First' garante que todas as funções críticas rodem 100% em hardware local. Os dados sincronizam automaticamente quando a conectividade é restaurada.",
            faqQ3: "Qual hardware é necessário?",
            faqA3: "Nossa plataforma usa hardware específico (nós Mac Studio M3 Ultra). Isso permite uma IA local poderosa com enorme economia de energia, totalmente gerenciada pela Voither.",
            faqQ4: "A Voither substitui nosso Prontuário Eletrônico (PEP)?",
            faqA4: "Não. A Voither é uma camada não disruptiva que se integra e aprimora seu PEP existente com automação inteligente, sem exigir uma migração custosa.",
            faqQ5: "Voither, HealthOS e Sortio?",
            faqA5: "Voither é a empresa e nossa infraestrutura de Edge Cloud. HealthOS é o SO seguro. O Mestral Engine é o 'cérebro' de IA. Sortio é nossa plataforma de saúde pública que usa toda a stack.",
            faqQ6: "Por que o HealthOS é uma parte central da stack?",
            faqA6: "SOs padrão não são construídos para IA de missão crítica em tempo real. O HealthOS é feito sob medida para garantir a estabilidade e segurança para fluxos de trabalho clínicos autônomos.",
            faqQ7: "Isso é só para lugares com internet ruim?",
            faqA7: "Não. É uma escolha estratégica para qualquer unidade que priorize privacidade de dados, resiliência e a performance em tempo real necessária para a verdadeira automação. É sobre autonomia.",
            faqQ8: "Como o modelo 'all-in-one' nos beneficia?",
            faqA8: "Ao entregar uma solução 'turnkey' totalmente gerenciada, eliminamos a complexidade, reduzimos seu TCO e garantimos performance, segurança e resiliência.",

            chatbotTitle: "Assistente de IA Voither",
            chatbotGreeting: "Olá! Como posso ajudar a entender a tecnologia da Voither?",
            chatbotPlaceholder: "Pergunte sobre nossa tecnologia...",
            copyright: "&copy; 2025 VOITHER. Todos os direitos reservados.",

            cookieConsentText: "Usamos cookies para aprimorar sua experiência de navegação e analisar nosso tráfego. Ao clicar em 'Aceitar', você concorda com nosso uso de cookies.",
            cookieAccept: "Aceitar",
            cookieDecline: "Recusar",
        }
    };

    let currentLang = localStorage.getItem('lang') || 'en';

    const setLanguage = (lang: string) => {
        if (!translations[lang]) return;
        currentLang = lang;
        localStorage.setItem('lang', lang);

        document.querySelectorAll<HTMLElement>('[data-key]').forEach(element => {
            const key = element.dataset.key;
            if (key && translations[lang][key]) {
                element.innerHTML = translations[lang][key];
            }
        });
        
        document.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>('[data-key^="formPlaceholder"], [data-key="faqPlaceholder"]').forEach(element => {
            const key = element.dataset.key;
             if (key && translations[lang][key]) {
                element.placeholder = translations[lang][key];
            }
        });
        
        const langSwitcher = document.querySelector('.lang-switcher');
        if (langSwitcher) langSwitcher.textContent = lang.toUpperCase();
        
        document.documentElement.lang = lang;
    };


    // --- Active Nav Link on Scroll ---
    const sections = document.querySelectorAll<HTMLElement>('section[id]');
    const navLinks = document.querySelectorAll('.sidebar-nav a');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.4
    };

    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        sectionObserver.observe(section);
    });
    
    // --- Scroll Animations ---
    const animatedElements = document.querySelectorAll('.architecture-pillar-card, .impact-card, .solution-pair, .research-card');
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(el => scrollObserver.observe(el));
    
    
    // --- Mobile Menu ---
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    mobileMenuToggle?.addEventListener('click', () => {
        const isExpanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true';
        mobileMenuToggle.setAttribute('aria-expanded', String(!isExpanded));
        mobileMenuToggle.classList.toggle('active');
        document.body.classList.toggle('sidebar-open');
    });

    // Close sidebar when a link is clicked
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', () => {
            if (document.body.classList.contains('sidebar-open')) {
                mobileMenuToggle?.setAttribute('aria-expanded', 'false');
                mobileMenuToggle?.classList.remove('active');
                document.body.classList.remove('sidebar-open');
            }
        });
    });


    // --- Interactive FAQ ---
    const setupInteractiveFAQ = () => {
        const responseArea = document.getElementById('faq-response-area');
        const input = document.getElementById('faq-input') as HTMLInputElement;
        const sendBtn = document.getElementById('faq-send-btn') as HTMLButtonElement;
        const suggestedQuestionsContainer = document.getElementById('faq-suggested-questions');

        if (!responseArea || !input || !sendBtn || !suggestedQuestionsContainer) return;

        // Build knowledge base from translations
        const faqKeys = Object.keys(translations.en).filter(k => k.startsWith('faqQ'));
        
        const askQuestion = async (question: string) => {
             // On first question, add a class to hide the welcome message/suggestions
            if (!responseArea.classList.contains('conversation-started')) {
                responseArea.classList.add('conversation-started');
            }

            // Create and display the user's question safely
            const userQuestionDiv = document.createElement('div');
            userQuestionDiv.className = 'faq-user-question';
            const userLabel = document.createElement('span');
            userLabel.className = 'faq-label';
            userLabel.textContent = 'You';
            const userParagraph = document.createElement('p');
            userParagraph.textContent = question; // Safely sets text content
            userQuestionDiv.appendChild(userLabel);
            userQuestionDiv.appendChild(userParagraph);
            responseArea.appendChild(userQuestionDiv);

            // Create and display the bot's placeholder answer
            const botAnswerDiv = document.createElement('div');
            botAnswerDiv.className = 'faq-bot-answer';
            botAnswerDiv.innerHTML = `<span class="faq-label">Voither AI</span><p class="thinking">Thinking...</p>`;
            responseArea.appendChild(botAnswerDiv);
            
            responseArea.scrollTop = responseArea.scrollHeight; // Scroll to bottom

            sendBtn.disabled = true;
            input.disabled = true;

            try {
                const response = await ai.models.generateContent({
                    model: 'gemini-2.5-flash',
                    contents: question,
                });
                const answer = response.text;

                const answerParagraph = botAnswerDiv.querySelector('p');
                if (answerParagraph) {
                    answerParagraph.classList.remove('thinking');
                    answerParagraph.innerHTML = answer.replace(/\n/g, '<br>');
                }

            } catch (error) {
                console.error("FAQ AI Error:", error);
                const answerParagraph = botAnswerDiv.querySelector('p');
                if (answerParagraph) {
                    answerParagraph.classList.remove('thinking');
                    answerParagraph.textContent = `Sorry, I couldn't find an answer to that. Please try rephrasing your question.`;
                }
            } finally {
                sendBtn.disabled = false;
                input.disabled = false;
                input.focus();
                responseArea.scrollTop = responseArea.scrollHeight; // Scroll again after response
            }
        };
        
        const handleSubmit = () => {
            const question = input.value.trim();
            if (question) {
                askQuestion(question);
                input.value = '';
            }
        };

        sendBtn.addEventListener('click', handleSubmit);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleSubmit();
            }
        });

        // Populate suggested questions
        suggestedQuestionsContainer.innerHTML = '';
        faqKeys.forEach(key => {
            const button = document.createElement('button');
            button.className = 'faq-suggestion-btn';
            button.textContent = translations[currentLang][key];
            button.addEventListener('click', () => {
                const questionText = button.textContent;
                if(questionText) askQuestion(questionText);
            });
            suggestedQuestionsContainer.appendChild(button);
        });
    };
    
    // --- Application Tabs ---
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabLinks.forEach(link => {
        link.addEventListener('click', () => {
            const tabId = link.getAttribute('data-tab');

            tabLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === tabId) {
                    pane.classList.add('active');
                }
            });
        });
    });
    
    // --- Contact Form ---
    const contactForm = document.getElementById('contact-form');
    const successMessage = document.getElementById('form-success-message');

    contactForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        // Here you would typically send form data to a server
        // For this demo, we'll just show the success message
        if(contactForm && successMessage) {
            contactForm.style.display = 'none';
            successMessage.style.display = 'block';
        }
    });
    
     // --- Chatbot UI Logic ---
    const setupChatbotUI = () => {
        const chatbotContainer = document.getElementById('chatbot-container');
        const openButtons = document.querySelectorAll('.js-open-chat');
        const closeButton = document.getElementById('chatbot-close-button');
        const overlay = document.getElementById('chatbot-overlay');
        // FIX: Cast sendButton to HTMLButtonElement to access the 'disabled' property.
        const sendButton = document.getElementById('chatbot-send-button') as HTMLButtonElement;
        const input = document.getElementById('chatbot-input') as HTMLInputElement;
        const messagesContainer = document.getElementById('chatbot-messages');

        if (!chatbotContainer || !closeButton || !overlay || !sendButton || !input || !messagesContainer) return;

        const openChat = () => chatbotContainer.classList.add('visible');
        const closeChat = () => chatbotContainer.classList.remove('visible');

        openButtons.forEach(btn => btn.addEventListener('click', openChat));
        closeButton.addEventListener('click', closeChat);
        overlay.addEventListener('click', closeChat);
        
        const showTypingIndicator = () => {
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'chat-message bot-message typing-indicator';
            typingIndicator.innerHTML = '<div class="message-content"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
            messagesContainer.appendChild(typingIndicator);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        };

        const removeTypingIndicator = () => {
            const indicator = messagesContainer.querySelector('.typing-indicator');
            if (indicator) {
                messagesContainer.removeChild(indicator);
            }
        };

        const handleSendMessage = async () => {
            const userMessage = input.value.trim();
            if (!userMessage) return;

            addMessage(userMessage, 'user');
            input.value = '';
            input.disabled = true;
            sendButton.disabled = true;

            showTypingIndicator();

            try {
                if (!chat) initializeChat(); // Ensure chat is initialized
                if (chat) {
                    const response = await chat.sendMessage({ message: userMessage });
                    const botResponse = response.text; // Use the direct .text property
                    removeTypingIndicator();
                    addMessage(botResponse.replace(/\n/g, '<br>'), 'bot');
                } else {
                     throw new Error("Chat could not be initialized.");
                }
            } catch (error) {
                console.error("Error sending message:", error);
                removeTypingIndicator();
                addMessage("Sorry, I'm having trouble connecting right now. Please try again later.", 'bot');
            } finally {
                 input.disabled = false;
                 sendButton.disabled = false;
                 input.focus();
            }
        };

        sendButton.addEventListener('click', handleSendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleSendMessage();
            }
        });
        
        addMessage(translations[currentLang].chatbotGreeting || "Hello! How can I help you understand Voither's technology?", 'bot');
    };
    
    // --- Technology Diagram Modal ---
    const setupInfoModal = () => {
        const modalContainer = document.getElementById('info-modal-container');
        const modal = document.getElementById('info-modal');
        const closeButton = document.getElementById('info-modal-close-button');
        const overlay = document.getElementById('info-modal-overlay');
        const titleEl = document.getElementById('info-modal-title');
        const descEl = document.getElementById('info-modal-description');
        const triggerButtons = document.querySelectorAll('[data-modal-target]');

        if (!modalContainer || !modal || !closeButton || !overlay || !titleEl || !descEl) return;
        
        const modalContent: { [key: string]: { titleKey: string; descKey: string } } = {
            'voither': { titleKey: 'stackVoitherTitle', descKey: 'modalVoitherCloudDesc' },
            'healthos': { titleKey: 'stackHealthOSTitle', descKey: 'modalHealthOSDesc' },
            'mestral': { titleKey: 'stackMestralTitle', descKey: 'modalMestralEngineDesc' },
            'pir': { titleKey: 'mestralPIRTitle', descKey: 'mestralPIRDesc' },
            'roe': { titleKey: 'mestralROETitle', descKey: 'mestralROEDesc' },
            'rms': { titleKey: 'mestralRMSTitle', descKey: 'mestralRMSDesc' },
            'rre': { titleKey: 'mestralRRETitle', descKey: 'mestralRREDesc' },
            'mdl': { titleKey: 'mestralMDLTitle', descKey: 'mestralMDLDesc' },
        };

        const openModal = (target: string) => {
            const content = modalContent[target];
            if (content && translations[currentLang]) {
                titleEl.textContent = translations[currentLang][content.titleKey] || '';
                descEl.innerHTML = translations[currentLang][content.descKey] || '';
                modalContainer.classList.add('visible');
            }
        };

        const closeModal = () => {
            modalContainer.classList.remove('visible');
        };

        triggerButtons.forEach(button => {
            button.addEventListener('click', () => {
                const target = (button as HTMLElement).dataset.modalTarget;
                if(target) openModal(target);
            });
        });

        closeButton.addEventListener('click', closeModal);
        overlay.addEventListener('click', closeModal);
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modalContainer.classList.contains('visible')) {
                closeModal();
            }
        });
    };
    
    // --- Cookie Consent Banner ---
    const setupCookieConsent = () => {
        const banner = document.getElementById('cookie-consent-banner');
        const acceptBtn = document.getElementById('cookie-accept-btn');
        const declineBtn = document.getElementById('cookie-decline-btn');

        if (!banner || !acceptBtn || !declineBtn) return;
        
        const consent = localStorage.getItem('cookie_consent');
        
        // If consent is already given or denied, do nothing.
        if(consent) return;

        // Otherwise, show the banner.
        setTimeout(() => {
            banner.classList.remove('hidden');
        }, 2000); // Show after 2 seconds

        const handleConsent = (value: 'accepted' | 'declined') => {
            localStorage.setItem('cookie_consent', value);
            banner.classList.add('hidden');
        };

        acceptBtn.addEventListener('click', () => handleConsent('accepted'));
        declineBtn.addEventListener('click', () => handleConsent('declined'));
    };
    
    // --- Header Scroll Effect ---
    const setupHeaderScroll = () => {
        const header = document.querySelector('.main-header');
        if (!header) return;

        const handleScroll = () => {
            if (window.scrollY > 20) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
    };

    // --- Initialization ---
    const init = () => {
        applyFeatureFlags();
        setLanguage(currentLang);
        
        const langSwitcher = document.querySelector('.lang-switcher');
        langSwitcher?.addEventListener('click', () => {
            const newLang = currentLang === 'en' ? 'pt' : 'en';
            setLanguage(newLang);
            
            if (chat) {
                initializeChat(); 
                const messagesContainer = document.getElementById('chatbot-messages');
                if (messagesContainer) {
                    messagesContainer.innerHTML = '';
                     addMessage(translations[currentLang].chatbotGreeting || "Hello! How can I help you understand Voither's technology?", 'bot');
                }
            }
            
            const faqResponseArea = document.getElementById('faq-response-area');
            if(faqResponseArea) {
                faqResponseArea.classList.remove('conversation-started');
                faqResponseArea.innerHTML = `
                    <p class="faq-welcome" data-key="faqWelcome">${translations[newLang].faqWelcome}</p>
                    <div id="faq-suggested-questions" class="faq-suggested-questions"></div>
                `;
                 const newWelcome = faqResponseArea.querySelector<HTMLElement>('[data-key="faqWelcome"]');
                 if (newWelcome) {
                     newWelcome.textContent = translations[newLang].faqWelcome;
                 }
            }
            setupInteractiveFAQ();
        });
        
        setupHeaderScroll();
        setupInfoModal();
        setupInteractiveFAQ();
        if (isFeatureEnabled('chatbot')) {
            setupChatbotUI();
        }
        setupCookieConsent();

        if (window.lucide) {
            window.lucide.createIcons({
                attrs: {
                    'stroke-width': 1.75,
                }
            });
        }
    };

    init();
});
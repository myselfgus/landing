/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
document.addEventListener("DOMContentLoaded", () => {
    
    // --- Translations and Language Switcher ---
    const translations = {
        en: {
            pageTitle: "Voither | Real-time Clinical Intelligence",
            proudlyPartOf: "Proudly member of",
            msForStartups: "Microsoft for Startups",
            santanderX: "Santander X",
            mongoDBAtlas: "MongoDB Atlas",
            
            heroTitleNew: "Focus on Your Patient,<br>Not the Paperwork.",
            heroPitchNew: "VOITHER MedicalScribe is your invisible AI partner, automating clinical documentation so you can dedicate your time to what truly matters: patient care.",
            heroInvestorsButton: "Investors",
            heroDevButton: "Developers",
            heroHealthButton: "Health Professionals",

            sectionTitleHowItWorks: "How It Works",
            sectionTitleTechnology: "The Voither Difference",
            sectionTitleUpdates: "Augmented-AI for Healthcare",
            navTitleAbout: "About Voither",
            navContact: "Contact & FAQ",
            medscribeButton: "MEDSCRIBE",
            holofractorButton: "HOLOFRACTOR",
            peeraiButton: "PEER-AI",
            viewAll: "View all",

            feature1Title: "Clinical Time as a 1st Class Citizen (kairos)",
            feature1Desc: "It's not just what to do; it's when to intervene—supported by signals from context and session rhythm.",
            feature2Title: "Compliance that Compiles (.ee)",
            feature2Desc: "Policies and standards (IEC 62304, HIPAA, FHIR) become code; if violated, it won't pass the build.",
            feature3Title: "Rhizomatic Memory + Signal Layers",
            feature3Desc: "A knowledge graph + vector representations + time series, with configurable encryption and retention.",
            feature4Title: "Native Clinical Automation (ReEngine)",
            feature4Desc: "Clinical workflows with ROI per session and scaling guided by clinical metrics, not just CPU.",
            
            howItWorksStep1Title: "You Talk.",
            howItWorksStep1Desc: "The MED extracts clinical signals from speech (mood, energy, coherence, flexibility, agency, prosody...).",
            howItWorksStep2Title: "Rhythm and Lived Time.",
            howItWorksStep2Desc: "The BRRE engine weaves signals over time, maintains competing hypotheses, and indicates 'what changed' and when to act—with justification.",
            howItWorksStep3Title: "Clinical Translation.",
            howItWorksStep3Desc: "Calibration to frameworks like RDoC/HiTOP/Big Five/PERMA, providing a common language for the team.",
            howItWorksStep4Title: "Automatic Action.",
            howItWorksStep4Desc: "AUTOAGENCY executes documentation, orders, scheduling, and billing—with auditing and measured time savings.",
            howItWorksResultTitle: "Visible Result.",
            howItWorksResultDesc: "A clear before/after, proposed paths with pros/cons, and the paperwork ready—all in seconds.",

            techPane1Title: "BRRE Engine",
            techPane3Title: "E2E Pipeline",
            
            techPane1Desc: "A reasoning engine that operates in lived time, not just clock time. It detects *when* to act (kairos), not just *what* to do.",
            techPane3Desc: "A pipeline that connects speech to signal, decision, and paperwork in seconds, with measurable ROI.",

            pioneer1Title: "Your Invisible Secretary",
            pioneer1Desc: "Voither anticipates administrative tasks like renewing prescriptions, sending reminders, and pre-filling progress notes before you even ask.",
            pioneer2Title: "The Patient's Digital Twin",
            pioneer2Desc: "Between consultations, the system non-invasively observes the patient's rhythm, identifying the best intervention windows and preparing insights for the next session.",
            pioneer3Title: "Ecosystem of Automations",
            pioneer3Desc: "A future marketplace of 'automation packages' will allow you to activate validated protocols with one click, complete with built-in efficacy metrics and auditing.",
            pioneer4Title: "Real-World Outcome Indicators",
            pioneer4Desc: "Not just 'what to do,' but whether it worked—and for whom it works best—in a way that is simple to demonstrate.",
            
            thesis: `"Today, a clinic talks and writes—but systems only understand checkboxes. Voither is born to listen to human language, turn it into objective signals, and act, with no learning curve. This is only possible because we bring together three things that almost no one has in the same place: a reasoning engine 'with time inside' (BRRE), proprietary languages that turn law into code (.ee), and a timed E2E pipeline from conversation to action."`,
            quoteAttribution: "— Founder & CEO, Voither",

            contactTitle: "Get in Touch",
            contactSubtitle: "Have questions or want to see a personalized demo? We’d love to hear from you.",
            contactButton: "Contact Us",
            faqTitle: "Frequently Asked Questions",
            faqQ1: "How does Voither ensure patient data privacy?",
            faqA1: "Voither is built with a 'compliance that compiles' philosophy. Privacy and security rules (like HIPAA and LGPD) are embedded directly into our proprietary language (.ee). This means any code that violates these rules simply won't compile, ensuring security by design, not as an afterthought. All data is encrypted both in transit and at rest.",
            faqQ2: "Does it integrate with existing Electronic Health Records (EHRs)?",
            faqA2: "Yes. Integration is a core part of our design. Voither uses the FHIR R4 standard to communicate seamlessly with modern EHR systems. Our E2E Pipeline is built to push structured documentation, orders, and billing information directly into your existing workflow, minimizing disruption.",
            faqQ3: "What is the learning curve for a clinician?",
            faqA3: "Virtually zero. Voither is designed to disappear into the background. The clinician just needs to have a natural conversation. The system listens, analyzes, and surfaces insights and automations without requiring complex training or changes to how you interact with a patient.",
            faqQ4: "How is 'clinical time' (kairos) different from normal analysis?",
            faqA4: "Most AI tools can tell you *what* was said. Our Bergsonian-Rhizomatic Reasoner Engine (BRRE) is designed to understand *when* to act. It analyzes the rhythm, intensity, and context of the conversation to identify opportune moments for intervention (kairos), a concept traditional chronological analysis misses entirely. It’s about clinical timing, not just a transcript.",
            
            complianceTitle: "Compliance",
            complianceLGPD: "LGPD",
            complianceHIPAA: "HIPAA",
            complianceFHIR: "FHIR",
            complianceRDoC: "RDoC",
            complianceHiTOP: "HiTOP",
            complianceBigFive: "BigFive",
            compliancePERMA: "PERMA",

            copyright: "© 2025 VOITHER. All rights reserved.",
        },
        pt: {
            pageTitle: "Voither | Inteligência Clínica em Tempo Real",
            proudlyPartOf: "Membro orgulhoso de",
            msForStartups: "Microsoft for Startups",
            santanderX: "Santander X",
            mongoDBAtlas: "MongoDB Atlas",

            heroTitleNew: "Foque no seu Paciente,<br>não na Papelada.",
            heroPitchNew: "O VOITHER MedicalScribe é seu parceiro de IA invisível, automatizando a documentação clínica para que você possa dedicar seu tempo ao que realmente importa: o cuidado com o paciente.",
            heroInvestorsButton: "Investidores",
            heroDevButton: "Desenvolvedores",
            heroHealthButton: "Profissionais de Saúde",
            
            sectionTitleHowItWorks: "Como Funciona",
            sectionTitleTechnology: "O Diferencial Voither",
            sectionTitleUpdates: "IA-Aumentada para Saúde",
            navTitleAbout: "Sobre a Voither",
            navContact: "Contato & FAQ",
            medscribeButton: "MEDSCRIBE",
            holofractorButton: "HOLOFRACTOR",
            peeraiButton: "PEER-AI",
            viewAll: "Ver tudo",

            feature1Title: "Tempo clínico como 1ª classe (kairos)",
            feature1Desc: "Não é só o que fazer; é quando intervir — sustentado por sinais do contexto e do ritmo da sessão.",
            feature2Title: "Compliance que compila (.ee)",
            feature2Desc: "Políticas e normas (IEC 62304, HIPAA, FHIR, LGPD) viram código; se violar, não passa no build.",
            feature3Title: "Memória rizomática + camadas de sinal",
            feature3Desc: "Grafo + representações vetoriais + séries temporais; criptografia e retenção configuráveis.",
            feature4Title: "Automação clínica nativa (ReEngine)",
            feature4Desc: "Workflows clínicos com ROI por sessão e escalonamento guiado por métrica clínica (não só CPU).",

            howItWorksStep1Title: "Você conversa.",
            howItWorksStep1Desc: "O MED extrai sinais clínicos da fala (humor, energia, coerência, flexibilidade, agência, prosódia…).",
            howItWorksStep2Title: "Ritmo e tempo vivido.",
            howItWorksStep2Desc: "O motor BRRE costura os sinais no tempo, mantém hipóteses concorrentes e indica “o que mudou” e quando agir — com justificativa.",
            howItWorksStep3Title: "Tradução clínica.",
            howItWorksStep3Desc: "Calibração para frameworks como RDoC/HiTOP/Big Five/PERMA, dando linguagem comum ao time.",
            howItWorksStep4Title: "Ação automática.",
            howItWorksStep4Desc: "AUTOAGENCY executa documentação, pedidos, agendamentos e billing — com auditoria e economia de tempo medidas.",
            howItWorksResultTitle: "Resultado visível.",
            howItWorksResultDesc: "Antes/depois claro, proposta de caminhos com prós/contras e a papelada pronta — tudo em segundos.",

            techPane1Title: "Motor BRRE",
            techPane3Title: "Pipeline E2E",
            
            techPane1Desc: "Um motor que raciocina no tempo vivido, não só no relógio. Ele detecta *quando* agir (kairos), não só *o que* fazer.",
            techPane3Desc: "Um pipeline que conecta fala a sinal, decisão e documentação em segundos, com ROI mensurável.",

            pioneer1Title: "Seu Secretário Invisível",
            pioneer1Desc: "O Voither antecipa tarefas administrativas como renovar receitas, lembrar retornos e pré-preencher evolutivos antes mesmo de você pedir.",
            pioneer2Title: "O Gêmeo Digital do Paciente",
            pioneer2Desc: "Entre consultas, o sistema observa o ritmo do paciente de forma não-invasiva, identificando as melhores janelas de intervenção e preparando insights para a próxima sessão.",
            pioneer3Title: "Ecossistema de Automações",
            pioneer3Desc: "Uma futura loja de 'pacotes de automação' permitirá ativar protocolos validados com um clique, com métricas de eficácia e auditoria embutidas.",
            pioneer4Title: "Indicadores de Desfecho no Mundo Real",
            pioneer4Desc: "Não só 'o que fazer', mas se funcionou — e para quem funciona melhor — de forma simples de demonstrar.",

            thesis: `"Hoje, a clínica conversa e escreve — mas os sistemas só entendem checkboxes. A Voither nasce para ouvir a linguagem humana, transformar em sinais objetivos e agir, sem curva de aprendizado. Isso só é possível porque juntamos três coisas que quase ninguém tem no mesmo lugar: um motor de raciocínio 'com tempo dentro' (BRRE), linguagens próprias que viram lei em código (.ee) e um pipeline E2E cronometrado da conversa à ação."`,
            quoteAttribution: "— Fundador & CEO, Voither",
            
            contactTitle: "Entre em Contato",
            contactSubtitle: "Tem perguntas ou quer ver uma demonstração personalizada? Adoraríamos ouvir você.",
            contactButton: "Fale Conosco",
            faqTitle: "Perguntas Frequentes",
            faqQ1: "Como a Voither garante a privacidade dos dados dos pacientes?",
            faqA1: "A Voither foi construída com a filosofia de 'compliance que compila'. Regras de privacidade e segurança (como HIPAA e LGPD) são incorporadas diretamente em nossa linguagem proprietária (.ee). Isso significa que qualquer código que viole essas regras simplesmente não compila, garantindo a segurança por design, não como um adendo. Todos os dados são criptografados em trânsito e em repouso.",
            faqQ2: "A plataforma se integra com Prontuários Eletrônicos (PEP/EHR) existentes?",
            faqA2: "Sim. A integração é parte central do nosso design. A Voither usa o padrão FHIR R4 para se comunicar de forma transparente com sistemas de PEP modernos. Nosso Pipeline E2E foi construído para enviar documentação estruturada, pedidos e informações de faturamento diretamente para o seu fluxo de trabalho existente, minimizando interrupções.",
            faqQ3: "Qual é a curva de aprendizado para um clínico?",
            faqA3: "Virtualmente zero. A Voither foi projetada para desaparecer no fundo. O clínico só precisa ter uma conversa natural. O sistema escuta, analisa e apresenta insights e automações sem exigir treinamento complexo ou mudanças na forma como você interage com os pacientes.",
            faqQ4: "Como o 'tempo clínico' (kairos) se difere da análise normal?",
            faqA4: "A maioria das ferramentas de IA pode dizer *o que* foi dito. Nosso Motor de Raciocínio Bergsoniano-Rizomático (BRRE) foi projetado para entender *quando* agir. Ele analisa o ritmo, a intensidade e o contexto da conversa para identificar momentos oportunos de intervenção (kairos), um conceito que a análise cronológica tradicional ignora completamente. Trata-se do timing clínico, não apenas de uma transcrição.",
            
            complianceTitle: "Conformidade",
            complianceLGPD: "LGPD",
            complianceHIPAA: "HIPAA",
            complianceFHIR: "FHIR",
            complianceRDoC: "RDoC",
            complianceHiTOP: "HiTOP",
            complianceBigFive: "BigFive",
            compliancePERMA: "PERMA",

            copyright: "© 2025 VOITHER. Todos os direitos reservados.",
        },
    };
    
    type Language = keyof typeof translations;

    const langSwitcher = document.querySelector<HTMLButtonElement>('.lang-switcher');
    const translatableElements = document.querySelectorAll<HTMLElement>('[data-key]');

    const setLanguage = (lang: Language) => {
        if (!translations[lang]) return;

        translatableElements.forEach(element => {
            const key = element.dataset.key as keyof typeof translations[Language];
            if (key && translations[lang][key]) {
                const translation = translations[lang][key];
                
                if (key === 'navTitleAbout' && element.closest('.sidebar-nav')) {
                    element.textContent = translations[lang]['navTitleAbout'];
                } else if (translation.includes('<') && translation.includes('>')) {
                    element.innerHTML = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
        
        document.documentElement.lang = lang;
        if (langSwitcher) {
            langSwitcher.textContent = lang.toUpperCase();
        }
        localStorage.setItem('voither-lang', lang);
    };

    if (langSwitcher) {
        langSwitcher.addEventListener('click', () => {
            const currentLang = (document.documentElement.lang as Language) || 'en';
            const newLang: Language = currentLang === 'en' ? 'pt' : 'en';
            setLanguage(newLang);
        });
    }

    // --- Theme Switcher Logic ---
    const themeSwitcher = document.querySelector<HTMLButtonElement>('.theme-switcher');
    const body = document.body;

    const applyTheme = (theme: string) => {
        if (theme === 'light') {
            body.classList.add('light-theme');
        } else {
            body.classList.remove('light-theme');
        }
    };

    const savedTheme = localStorage.getItem('voither-theme');
    // Default to light theme. Only use dark theme if it's explicitly saved.
    if (savedTheme === 'dark') {
        applyTheme('dark');
    } else {
        applyTheme('light');
    }

    if (themeSwitcher) {
        themeSwitcher.addEventListener('click', () => {
            const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
            localStorage.setItem('voither-theme', newTheme);
            applyTheme(newTheme);
        });
    }
    
    // --- Mobile Menu Logic ---
    const mobileMenuToggle = document.querySelector<HTMLButtonElement>('.mobile-menu-toggle');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            const isOpened = body.classList.toggle('sidebar-open');
            mobileMenuToggle.setAttribute('aria-expanded', isOpened.toString());
            mobileMenuToggle.classList.toggle('active', isOpened);
        });
    }

    // --- Scroll Handlers ---
    const sections = document.querySelectorAll<HTMLElement>('section[id]');
    const navLinks = document.querySelectorAll<HTMLAnchorElement>('.sidebar-nav a');

    const handleScroll = () => {
        // Activate sidebar nav link
        let currentSectionId = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - 150) {
                currentSectionId = section.getAttribute('id') || '';
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSectionId}`) {
                link.classList.add('active');
            }
        });
        
        // Add scrolled class to body for styling header/sidebar
        if (window.scrollY > 10) {
            body.classList.add('scrolled');
        } else {
            body.classList.remove('scrolled');
        }
    };
    
    // --- FAQ Accordion Logic ---
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer') as HTMLElement | null;

        if (question && answer) {
            question.addEventListener('click', () => {
                const wasActive = item.classList.contains('active');
                
                // Close all other items before opening a new one
                faqItems.forEach(i => {
                    if (i !== item) {
                        i.classList.remove('active');
                        (i.querySelector('.faq-answer') as HTMLElement).style.maxHeight = '0px';
                    }
                });

                // Toggle the clicked item
                if (!wasActive) {
                    item.classList.add('active');
                    answer.style.maxHeight = `${answer.scrollHeight}px`;
                } else {
                    item.classList.remove('active');
                    answer.style.maxHeight = '0px';
                }
            });
        }
    });

    // --- Animation on Scroll ---
    const animatedElements = document.querySelectorAll('.tech-card, .timeline-item');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(el => {
        observer.observe(el);
    });


    // --- Initial Language Load ---
    const savedLang = localStorage.getItem('voither-lang') as Language | null;
    const initialLang: Language = savedLang || 'en';
    setLanguage(initialLang);
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
});
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { GoogleGenAI, Chat } from "@google/genai";

document.addEventListener("DOMContentLoaded", () => {

    // --- Gemini Chatbot ---
    let chat: Chat | null = null;
    const ai = new GoogleGenAI({apiKey: process.env.API_KEY});

    const initializeChat = () => {
        const systemInstruction = `You are a helpful and friendly assistant for Voither, a company specializing in AI for clinical intelligence. 
        Your goal is to answer questions about the company, its products (like MEDSCRIBE, HOLOFRACTOR, PEER-AI), and its technology. 
        Keep your answers concise, informative, and maintain a professional but approachable tone. 
        If you don't know an answer, say that you don't have that information.`;
        
        chat = ai.chats.create({
            model: 'gemini-2.5-flash',
            config: {
                systemInstruction: systemInstruction,
            },
        });
    };
    
    // --- Smooth Scroll Polyfill for older browsers ---
    // The `html` element has `scroll-behavior: smooth` in CSS. This JS snippet
    // acts as a polyfill for browsers that do not support this property.
    const isSmoothScrollSupported = 'scrollBehavior' in document.documentElement.style;

    if (!isSmoothScrollSupported) {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (this: HTMLAnchorElement, e: MouseEvent) {
                const hrefAttr = this.getAttribute('href');
                // Ensure it's a valid on-page link
                if (!hrefAttr || hrefAttr.length <= 1) return;

                const targetElement = document.querySelector(hrefAttr);
                if (targetElement) {
                    e.preventDefault();
                    
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                    const startPosition = window.pageYOffset;
                    const distance = targetPosition - startPosition;
                    let startTime: number | null = null;
                    const duration = 800; // ms

                    const easeInOutQuad = (t: number, b: number, c: number, d: number) => {
                        t /= d / 2;
                        if (t < 1) return c / 2 * t * t + b;
                        t--;
                        return -c / 2 * (t * (t - 2) - 1) + b;
                    };

                    const animation = (currentTime: number) => {
                        if (startTime === null) startTime = currentTime;
                        const timeElapsed = currentTime - startTime;
                        const run = easeInOutQuad(timeElapsed, startPosition, distance, duration);
                        window.scrollTo(0, run);
                        if (timeElapsed < duration) {
                            requestAnimationFrame(animation);
                        } else {
                            // After scrolling, update the hash in the URL
                            if (history.pushState) {
                                history.pushState(null, '', hrefAttr);
                            } else {
                                window.location.hash = hrefAttr;
                            }
                        }
                    };
                    
                    requestAnimationFrame(animation);
                }
            });
        });
    }

    // --- Translations and Language Switcher ---
    const translations = {
        en: {
            pageTitle: "Voither | Real-time Clinical Intelligence",
            proudlyPartOf: "Proudly member of",
            msForStartups: "Microsoft for Startups",
            mongoDBAtlas: "MongoDB Atlas",
            
            heroPreTitle: "+150 patients monitored with impressive changes in clinical trajectories",
            heroTitleNew: "Focus on Your Patient,<br>Not the Paperwork.",
            heroPitchNew: "VOITHER MedicalScribe is your invisible AI partner, automating clinical documentation so you can dedicate your time to what truly matters: patient care.",
            heroInvestorsButton: "Investors",
            heroDevButton: "Developers",
            heroHealthButton: "Health Professionals",

            sectionTitleHowItWorks: "How It Works",
            sectionTitleTechnology: "The Voither Difference",
            sectionTitleUpdates: "Augmented-AI for Healthcare",
            navFeatures: "Features",
            navTestimonials: "Testimonials",
            navTitleAbout: "About Voither",
            navContact: "Contact & FAQ",
            medscribeButton: "MEDSCRIBE",
            holofractorButton: "HOLOFRACTOR",
            peeraiButton: "PEER-AI",
            viewAll: "View all",

            feature1Title: "Clinical Timing is Everything",
            feature1Desc: "It's not just what to do; it's when to intervene—supported by signals from context and session rhythm.",
            feature2Title: "Compliance by Design",
            feature2Desc: "Policies and standards (IEC 62304, HIPAA, FHIR) become code; if violated, it won't pass the build.",
            feature3Title: "Rhizomatic Memory + Signal Layers",
            feature3Desc: "A knowledge graph + vector representations + time series, with configurable encryption and retention.",
            feature4Title: "Native Clinical Automation",
            feature4Desc: "Clinical workflows with ROI per session and scaling guided by clinical metrics, not just CPU.",
            
            videoCaption: "Watch a 2-minute demo to see Voither in action.",
            howItWorksStep1Title: "You Talk.",
            howItWorksStep1Desc: "The MED extracts clinical signals from speech (mood, energy, coherence, flexibility, agency, prosody...).",
            howItWorksStep2Title: "Rhythm and Lived Time.",
            howItWorksStep2Desc: "Our advanced reasoning engine weaves signals over time, maintains competing hypotheses, and indicates 'what changed' and when to act—with justification.",
            howItWorksStep3Title: "Clinical Translation.",
            howItWorksStep3Desc: "Calibration to frameworks like RDoC/HiTOP/Big Five/PERMA, providing a common language for the team.",
            howItWorksStep4Title: "Automatic Action.",
            howItWorksStep4Desc: "AUTOAGENCY executes documentation, orders, scheduling, and billing—with auditing and measured time savings.",
            howItWorksResultTitle: "Visible Result.",
            howItWorksResultDesc: "A clear before/after, proposed paths with pros/cons, and the paperwork ready—all in seconds.",

            techPane1Title: "Temporal Reasoning Engine",
            techPane3Title: "E2E Pipeline",
            
            techPane1Desc: "A reasoning engine that operates in lived time, not just clock time. It detects *when* to act, not just *what* to do.",
            techPane3Desc: "A pipeline that connects speech to signal, decision, and paperwork in seconds, with measurable ROI.",

            pioneer1Title: "Your Invisible Secretary",
            pioneer1Desc: "Voither anticipates administrative tasks like renewing prescriptions, sending reminders, and pre-filling progress notes before you even ask.",
            pioneer2Title: "The Patient's Digital Twin",
            pioneer2Desc: "Between consultations, the system non-invasively observes the patient's rhythm, identifying the best intervention windows and preparing insights for the next session.",
            pioneer3Title: "Ecosystem of Automations",
            pioneer3Desc: "A future marketplace of 'automation packages' will allow you to activate validated protocols with one click, complete with built-in efficacy metrics and auditing.",
            pioneer4Title: "Real-World Outcome Indicators",
            pioneer4Desc: "Not just 'what to do,' but whether it worked—and for whom it works best—in a way that is simple to demonstrate.",
            
            sectionTitleTestimonials: "Trusted by Professionals",
            testimonial1Quote: "Voither has fundamentally changed how I approach documentation. It saves me over an hour a day, time I now spend directly with my patients. It's a game-changer.",
            testimonial1Name: "Maria Christina Luciano",
            testimonial1Title: "Clinical Psychologist",
            testimonial2Quote: "The accuracy of the clinical signal extraction is remarkable. It picks up on nuances that are easy to miss during a busy session, providing deeper insights for treatment planning.",
            testimonial2Name: "Dr. Ana Gabriela",
            testimonial2Title: "MD, Psychiatrist",
            testimonial3Quote: "As a clinic manager, the 'Compliance by Design' feature gives me peace of mind. Integrating Voither was seamless, and the ROI was clear from the first week.",
            testimonial3Name: "Simone Maria",
            testimonial3Title: "Healthcare Clinic Officer",
            
            aboutSectionTitle: "The Mind Behind Voither",
            founderName: "Dr. Gustavo Mendes",
            founderTitle: "Founder & CEO | CRM/SP 218133",
            founderBio: "Voither was founded by Dr. Gustavo Mendes e Silva, a psychiatrist (FAMEMA) and public administrator (UNESP). His unique journey combines deep clinical experience with a passion for systemic innovation, including work with the UN (UNFPA) and PAHO in Washington D.C., and winning the YouthAgainstAIDS Ahead Hackathon. Before Voither, he managed healthcare networks for São Paulo, witnessing the burdens that distract clinicians from patient care.",
            thesis: `"Today, a clinic talks and writes—but systems only understand checkboxes. Voither is born to listen to human language, turn it into objective signals, and act, with no learning curve. This is only possible because we bring together three things that almost no one has in the same place: a temporal reasoning engine that understands clinical rhythm, a proprietary architecture that turns compliance into code, and a timed E2E pipeline from conversation to action."`,
            quoteAttribution: "— Dr. Gustavo Mendes e Silva, Founder & CEO, Voither",

            contactTitle: "Send us a Message",
            contactSubtitle: "We'll get back to you as soon as possible.",
            formLabelName: "Full Name",
            formPlaceholderName: "Your Name",
            formLabelEmail: "Email Address",
            formPlaceholderEmail: "you@example.com",
            formLabelMessage: "Message",
            formPlaceholderMessage: "How can we help you today?",
            formSubmitButton: "Send Message",
            formSuccessTitle: "Thank You!",
            formSuccessMessage: "Your message has been sent. We'll be in touch shortly.",
            faqTitle: "Frequently Asked Questions",
            faqQ1: "How does Voither ensure patient data privacy?",
            faqA1: "Voither is built with a 'compliance by design' philosophy. Privacy and security rules (like HIPAA and LGPD) are embedded directly into our system's core architecture. This means any process that violates these rules simply won't execute, ensuring security by design, not as an afterthought. All data is encrypted both in transit and at rest.",
            faqQ2: "Does it integrate with existing Electronic Health Records (EHRs)?",
            faqA2: "Yes. Integration is a core part of our design. Voither uses the FHIR R4 standard to communicate seamlessly with modern EHR systems. Our E2E Pipeline is built to push structured documentation, orders, and billing information directly into your existing workflow, minimizing disruption.",
            faqQ3: "What is the learning curve for a clinician?",
            faqA3: "Virtually zero. Voither is designed to disappear into the background. The clinician just needs to have a natural conversation. The system listens, analyzes, and surfaces insights and automations without requiring complex training or changes to how you interact with a patient.",
            faqQ4: "How is 'clinical timing' different from normal analysis?",
            faqA4: "Most AI tools can tell you *what* was said. Our advanced reasoning engine is designed to understand *when* to act. It analyzes the rhythm, intensity, and context of the conversation to identify opportune moments for intervention, a concept traditional chronological analysis misses entirely. It’s about clinical timing, not just a transcript.",
            
            complianceTitle: "Compliance",
            complianceLGPD: "LGPD",
            complianceHIPAA: "HIPAA",
            complianceFHIR: "FHIR",
            complianceRDoC: "RDoC",
            complianceHiTOP: "HiTOP",
            complianceBigFive: "BigFive",
            compliancePERMA: "PERMA",

            copyright: "© 2025 VOITHER. All rights reserved.",
            
            // Chatbot translations
            chatbotTitle: "Voither Assistant",
            chatbotPlaceholder: "Ask about Voither...",
            chatbotInitialMessage: "Hello! I'm the Voither assistant. How can I help you learn about our clinical intelligence platform?",
            chatbotErrorMessage: "Sorry, I'm having trouble connecting. Please try again later.",
        },
        pt: {
            pageTitle: "Voither | Inteligência Clínica em Tempo Real",
            proudlyPartOf: "Membro orgulhoso de",
            msForStartups: "Microsoft for Startups",
            mongoDBAtlas: "MongoDB Atlas",

            heroPreTitle: "+150 pacientes acompanhados com mudanças impressionantes de trajetórias clínicas",
            heroTitleNew: "Foque no seu Paciente,<br>não na Papelada.",
            heroPitchNew: "O VOITHER MedicalScribe é seu parceiro de IA invisível, automatizando a documentação clínica para que você possa dedicar seu tempo ao que realmente importa: o cuidado com o paciente.",
            heroInvestorsButton: "Investidores",
            heroDevButton: "Desenvolvedores",
            heroHealthButton: "Profissionais de Saúde",
            
            sectionTitleHowItWorks: "Como Funciona",
            sectionTitleTechnology: "O Diferencial Voither",
            sectionTitleUpdates: "IA-Aumentada para Saúde",
            navFeatures: "Funcionalidades",
            navTestimonials: "Depoimentos",
            navTitleAbout: "Sobre a Voither",
            navContact: "Contato & FAQ",
            medscribeButton: "MEDSCRIBE",
            holofractorButton: "HOLOFRACTOR",
            peeraiButton: "PEER-AI",
            viewAll: "Ver tudo",

            feature1Title: "O Timing Clínico é Essencial",
            feature1Desc: "Não é só o que fazer; é quando intervir — sustentado por sinais do contexto e do ritmo da sessão.",
            feature2Title: "Compliance por Design",
            feature2Desc: "Políticas e normas (IEC 62304, HIPAA, FHIR, LGPD) viram código; se violar, não passa no build.",
            feature3Title: "Memória rizomática + camadas de sinal",
            feature3Desc: "Grafo + representações vetoriais + séries temporais; criptografia e retenção configuráveis.",
            feature4Title: "Automação clínica nativa",
            feature4Desc: "Workflows clínicos com ROI por sessão e escalonamento guiado por métrica clínica (não só CPU).",

            videoCaption: "Assista a uma demonstração de 2 minutos para ver a Voither em ação.",
            howItWorksStep1Title: "Você conversa.",
            howItWorksStep1Desc: "O MED extrai sinais clínicos da fala (humor, energia, coerência, flexibilidade, agência, prosódia…).",
            howItWorksStep2Title: "Ritmo e tempo vivido.",
            howItWorksStep2Desc: "Nosso motor de raciocínio avançado costura os sinais no tempo, mantém hipóteses concorrentes e indica “o que mudou” e quando agir — com justificativa.",
            howItWorksStep3Title: "Tradução clínica.",
            howItWorksStep3Desc: "Calibração para frameworks como RDoC/HiTOP/Big Five/PERMA, dando linguagem comum ao time.",
            howItWorksStep4Title: "Ação automática.",
            howItWorksStep4Desc: "AUTOAGENCY executa documentação, pedidos, agendamentos e billing — com auditoria e economia de tempo medidas.",
            howItWorksResultTitle: "Resultado visível.",
            howItWorksResultDesc: "Antes/depois claro, proposta de caminhos com prós/contras e a papelada pronta — tudo em segundos.",

            techPane1Title: "Motor de Raciocínio Temporal",
            techPane3Title: "Pipeline E2E",
            
            techPane1Desc: "Um motor que raciocina no tempo vivido, não só no relógio. Ele detecta *quando* agir, não só *o que* fazer.",
            techPane3Desc: "Um pipeline que conecta fala a sinal, decisão e documentação em segundos, com ROI mensurável.",

            pioneer1Title: "Seu Secretário Invisível",
            pioneer1Desc: "O Voither antecipa tarefas administrativas como renovar receitas, lembrar retornos e pré-preencher evolutivos antes mesmo de você pedir.",
            pioneer2Title: "O Gêmeo Digital do Paciente",
            pioneer2Desc: "Entre consultas, o sistema observa o ritmo do paciente de forma não-invasiva, identificando as melhores janelas de intervenção e preparando insights para a próxima sessão.",
            pioneer3Title: "Ecossistema de Automações",
            pioneer3Desc: "Uma futura loja de 'pacotes de automação' permitirá ativar protocolos validados com um clique, com métricas de eficácia e auditoria embutidas.",
            pioneer4Title: "Indicadores de Desfecho no Mundo Real",
            pioneer4Desc: "Não só 'o que fazer', mas se funcionou — e para quem funciona melhor — de forma simples de demonstrar.",
            
            sectionTitleTestimonials: "Aprovado por Profissionais",
            testimonial1Quote: "A Voither mudou fundamentalmente a forma como eu lido com a documentação. Economizo mais de uma hora por dia, tempo que agora dedico diretamente aos meus pacientes. É um divisor de águas.",
            testimonial1Name: "Maria Christina Luciano",
            testimonial1Title: "Psicóloga Clínica",
            testimonial2Quote: "A precisão da extração de sinais clínicos é notável. Ele capta nuances que são fáceis de perder durante uma sessão agitada, fornecendo insights mais profundos para o planejamento do tratamento.",
            testimonial2Name: "Dr. Ana Gabriela",
            testimonial2Title: "MD, Psiquiatra",
            testimonial3Quote: "Como gestora de uma clínica, a funcionalidade 'Compliance por Design' me dá tranquilidade. A integração da Voither foi perfeita e o ROI ficou claro desde a primeira semana.",
            testimonial3Name: "Simone Maria",
            testimonial3Title: "Supervisora de equipe de enfermagem",

            aboutSectionTitle: "A Mente por Trás da Voither",
            founderName: "Dr. Gustavo Mendes",
            founderTitle: "Fundador & CEO | CRM/SP 218133",
            founderBio: "A Voither foi fundada pelo Dr. Gustavo Mendes e Silva, médico psiquiatra (FAMEMA) e administrador público (UNESP). Sua jornada única combina profunda experiência clínica com uma paixão por inovação sistêmica, incluindo passagens pela ONU (UNFPA) e OPAS em Washington D.C., e a vitória no Ahead Hackathon da YouthAgainstAIDS. Antes da Voither, foi gestor de redes de saúde em São Paulo, onde testemunhou o peso administrativo que afasta os clínicos do cuidado ao paciente.",
            thesis: `"Hoje, a clínica conversa e escreve — mas os sistemas só entendem checkboxes. A Voither nasce para ouvir a linguagem humana, transformar em sinais objetivos e agir, sem curva de aprendizado. Isso só é possível porque juntamos três coisas que quase ninguém tem no mesmo lugar: um motor de raciocínio temporal que entende o ritmo clínico, uma arquitetura proprietária que transforma compliance em código, e um pipeline E2E cronometrado da conversa à ação."`,
            quoteAttribution: "— Dr. Gustavo Mendes e Silva, Fundador & CEO, Voither",
            
            contactTitle: "Envie-nos uma Mensagem",
            contactSubtitle: "Retornaremos o mais breve possível.",
            formLabelName: "Nome Completo",
            formPlaceholderName: "Seu Nome",
            formLabelEmail: "Endereço de E-mail",
            formPlaceholderEmail: "voce@exemplo.com",
            formLabelMessage: "Mensagem",
            formPlaceholderMessage: "Como podemos ajudar hoje?",
            formSubmitButton: "Enviar Mensagem",
            formSuccessTitle: "Obrigado!",
            formSuccessMessage: "Sua mensagem foi enviada. Entraremos em contato em breve.",
            faqTitle: "Perguntas Frequentes",
            faqQ1: "Como a Voither garante a privacidade dos dados dos pacientes?",
            faqA1: "A Voither foi construída com a filosofia de 'compliance por design'. Regras de privacidade e segurança (como HIPAA e LGPD) são incorporadas diretamente na arquitetura do nosso sistema. Isso significa que qualquer processo que viole essas regras simplesmente não é executado, garantindo a segurança por design, não como um adendo. Todos os dados são criptografados em trânsito e em repouso.",
            faqQ2: "A plataforma se integra com Prontuários Eletrônicos (PEP/EHR) existentes?",
            faqA2: "Sim. A integração é parte central do nosso design. A Voither usa o padrão FHIR R4 para se comunicar de forma transparente com sistemas de PEP modernos. Nosso Pipeline E2E foi construído para enviar documentação estruturada, pedidos e informações de faturamento diretamente para o seu fluxo de trabalho existente, minimizando interrupções.",
            faqQ3: "Qual é a curva de aprendizado para um clínico?",
            faqA3: "Virtualmente zero. A Voither foi projetada para desaparecer no fundo. O clínico só precisa ter uma conversa natural. O sistema escuta, analisa e apresenta insights e automações sem exigir treinamento complexo ou mudanças na forma como você interage com os pacientes.",
            faqQ4: "Como o 'timing clínico' da Voither se difere da análise convencional?",
            faqA4: "A maioria das ferramentas de IA pode dizer *o que* foi dito. Nosso motor de raciocínio avançado foi projetado para entender *quando* agir. Ele analisa o ritmo, a intensidade e o contexto da conversa para identificar momentos oportunos de intervenção, um conceito que a análise cronológica tradicional ignora completamente. Trata-se do timing clínico, não apenas de uma transcrição.",
            
            complianceTitle: "Conformidade",
            complianceLGPD: "LGPD",
            complianceHIPAA: "HIPAA",
            complianceFHIR: "FHIR",
            complianceRDoC: "RDoC",
            complianceHiTOP: "HiTOP",
            complianceBigFive: "BigFive",
            compliancePERMA: "PERMA",

            copyright: "© 2025 VOITHER. Todos os direitos reservados.",
            
            // Chatbot translations
            chatbotTitle: "Assistente Voither",
            chatbotPlaceholder: "Pergunte sobre a Voither...",
            chatbotInitialMessage: "Olá! Sou o assistente da Voither. Como posso ajudar você a conhecer nossa plataforma de inteligência clínica?",
            chatbotErrorMessage: "Desculpe, estou com problemas de conexão. Por favor, tente novamente mais tarde.",
        },
    };
    
    type Language = keyof typeof translations;

    const langSwitcher = document.querySelector<HTMLButtonElement>('.lang-switcher');
    const translatableElements = document.querySelectorAll<HTMLElement>('[data-key]');
    const chatMessagesContainer = document.getElementById('chatbot-messages') as HTMLElement;


    const setLanguage = (lang: Language) => {
        if (!translations[lang]) return;

        translatableElements.forEach(element => {
            const key = element.dataset.key as keyof typeof translations[Language];
            if (key && translations[lang][key]) {
                const translation = translations[lang][key];
                
                // Handle placeholders for input and textarea
                if ((element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') && element.hasAttribute('placeholder')) {
                    (element as HTMLInputElement | HTMLTextAreaElement).placeholder = translation;
                } else if (key === 'navTitleAbout' && element.closest('.sidebar-nav')) {
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

        // Update initial chatbot message if chat is visible
        if (chatMessagesContainer && chatMessagesContainer.children.length <= 1) {
            addBotMessage(translations[lang].chatbotInitialMessage);
        }
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
    const contentWrapper = document.querySelector<HTMLElement>('.content-wrapper');

    const closeSidebar = () => {
        if (body.classList.contains('sidebar-open')) {
            body.classList.remove('sidebar-open');
            if (mobileMenuToggle) {
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                mobileMenuToggle.classList.remove('active');
            }
        }
    };

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            const isOpened = body.classList.toggle('sidebar-open');
            mobileMenuToggle.setAttribute('aria-expanded', isOpened.toString());
            mobileMenuToggle.classList.toggle('active', isOpened);
        });
    }
    
    if (contentWrapper) {
        contentWrapper.addEventListener('click', closeSidebar);
    }

    // --- Scroll Handlers ---
    const sections = document.querySelectorAll<HTMLElement>('section[id]');
    const navLinks = document.querySelectorAll<HTMLAnchorElement>('.sidebar-nav a');

    // Close sidebar on nav link click (for mobile)
    navLinks.forEach(link => {
        link.addEventListener('click', closeSidebar);
    });

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
    const animatedElements = document.querySelectorAll('.tech-card, .timeline-item, .testimonial-card');
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

    // --- Form Submission Logic ---
    const contactForm = document.getElementById('contact-form') as HTMLFormElement | null;
    const successMessage = document.getElementById('form-success-message') as HTMLElement | null;
    const contactInfoContainer = document.querySelector('.contact-info');

    if (contactForm && successMessage && contactInfoContainer) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = contactForm.querySelector<HTMLInputElement>('#name')?.value;
            const email = contactForm.querySelector<HTMLInputElement>('#email')?.value;
            const message = contactForm.querySelector<HTMLTextAreaElement>('#message')?.value;

            if (name && email && message) {
                contactForm.style.display = 'none';
                
                const title = contactInfoContainer.querySelector<HTMLElement>('.section-title');
                const subtitle = contactInfoContainer.querySelector<HTMLElement>('.section-subtitle');
                if (title) title.style.display = 'none';
                if (subtitle) subtitle.style.display = 'none';

                successMessage.style.display = 'block';
            }
        });
    }

    // --- Chatbot Logic ---
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatBubbleButton = document.getElementById('chat-bubble-button');
    const chatbotCloseButton = document.getElementById('chatbot-close-button');
    const chatbotOverlay = document.getElementById('chatbot-overlay');
    const chatbotInput = document.getElementById('chatbot-input') as HTMLInputElement;
    const chatbotSendButton = document.getElementById('chatbot-send-button');

    const toggleChatbot = (show: boolean) => {
        if (show) {
            chatbotContainer?.classList.add('visible');
            chatbotInput?.focus();
            if (chatMessagesContainer && chatMessagesContainer.children.length === 0) {
                 const currentLang = (document.documentElement.lang as Language) || 'en';
                 addBotMessage(translations[currentLang].chatbotInitialMessage);
            }
        } else {
            chatbotContainer?.classList.remove('visible');
        }
    };
    
    const addMessage = (content: string, type: 'user' | 'bot') => {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = `chat-message ${type}-message`;
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        messageWrapper.appendChild(messageContent);
        chatMessagesContainer?.appendChild(messageWrapper);
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    };
    
    const addBotMessage = (content: string) => addMessage(content, 'bot');
    const addUserMessage = (content: string) => addMessage(content, 'user');

    const showTypingIndicator = () => {
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'chat-message bot-message';
        typingIndicator.id = 'typing-indicator';
        typingIndicator.innerHTML = `
            <div class="message-content typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>`;
        chatMessagesContainer?.appendChild(typingIndicator);
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    };

    const removeTypingIndicator = () => {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    };
    
    const handleSendMessage = async () => {
        const message = chatbotInput.value.trim();
        if (!message) return;

        addUserMessage(message);
        chatbotInput.value = '';
        showTypingIndicator();

        try {
            if (!chat) initializeChat();
            if (!chat) throw new Error("Chat not initialized");

            const response = await chat.sendMessage({ message });
            
            removeTypingIndicator();
            addBotMessage(response.text);

        } catch (error) {
            console.error("Gemini API Error:", error);
            const currentLang = (document.documentElement.lang as Language) || 'en';
            removeTypingIndicator();
            addBotMessage(translations[currentLang].chatbotErrorMessage);
        }
    };

    chatBubbleButton?.addEventListener('click', () => toggleChatbot(true));
    chatbotCloseButton?.addEventListener('click', () => toggleChatbot(false));
    chatbotOverlay?.addEventListener('click', () => toggleChatbot(false));
    chatbotSendButton?.addEventListener('click', handleSendMessage);
    chatbotInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // --- Initial Language Load ---
    const savedLang = localStorage.getItem('voither-lang') as Language | null;
    const initialLang: Language = savedLang || 'en';
    setLanguage(initialLang);
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
});
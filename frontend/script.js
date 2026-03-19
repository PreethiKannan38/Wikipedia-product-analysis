const contentData = {
    home: {
        title: "Wikipedia Product Analysis Dashboard",
        subtitle: "Comprehensive analysis of pageviews, editor trends, and social sentiment (2015–2025)",
        html: `
            <div class="wiki-box">
                <p><strong>Welcome to the Wikipedia Product Analysis Dashboard.</strong> This project explores the health and reach of Wikipedia through multi-dimensional data analysis.</p>
                <p>Navigate through the menu on the left to explore different facets of the analysis, including:</p>
                <ul>
                    <li><strong>Pageview Analysis:</strong> Interactive trends and seasonality analysis of Wikipedia traffic across time.</li>
                    <li><strong>Reddit Sentiment Analysis:</strong> Insights into public perception of Wikipedia and ChatGPT based on Reddit discussions.</li>
                    <li><strong>Twitter Sentiment Analysis:</strong> Analysis of public sentiment on Twitter regarding Wikipedia.</li>
                </ul>
            </div>
        `
    },
    pageviews: {
        title: "Wikipedia Pageview Analysis (2015–2025)",
        subtitle: "Interactive Tableau Dashboard for regional and platform-level insights",
        html: `
            <div class="dashboard-container">
                <div class='tableauPlaceholder' id='viz1773934367186' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;wi&#47;wikipediapageviewanalysis&#47;pageviewanalysis&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='wikipediapageviewanalysis&#47;pageviewanalysis' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;wi&#47;wikipediapageviewanalysis&#47;pageviewanalysis&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1773934367186');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='1000px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='850px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='1000px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='850px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1400px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
            </div>
            <div class="wiki-box insights-section">
                <h2>Data Insights & Analysis</h2>
                <div class="insight-item">
                    <h3>1. Weekend vs Weekday Usage</h3>
                        <p>
                            Wikipedia was primarily a <strong>weekday-driven utility before 2020</strong>, with higher activity during school and workdays (ratio &lt; 1.0). Over time, the ratio steadily increases and crosses 1.0 during the pandemic, remaining above it, indicating rising weekend activity. This suggests an evolving usage pattern, where <strong>remote and flexible work may have shifted traditional school- and work-driven traffic spikes</strong>.
                        </p>
                    <h3>2. Wikipedia Seasonality</h3>
                        <p>
                            Wikipedia traffic shows a <strong>stable seasonal pattern with a strong baseline (7–8B pageviews)</strong>, where <strong>June consistently records the lowest pageviews and January shows comparatively higher activity</strong>, reflecting predictable user behavior cycles. Wikipedia’s traffic demonstrates <strong>dual drivers</strong>: a stable seasonal structure tied to academic calendars and information-seeking behavior, combined with <strong>unpredictable spikes from major world events</strong>, highlighting its resilience in maintaining a consistent multi-billion pageview baseline despite external shocks. However, recent years indicate a <strong>slight downward shift from the 2020–2022 peak</strong>, suggesting normalization after pandemic-driven demand, with a <strong>minor emerging influence of AI-mediated information access</strong> shaping future growth.
                        </p>
                    <h3>3. Campaign Impact on Traffic</h3>
                        <p>
                            Across campaign types, pageview lift remains within a relatively narrow range (around -6% to +7%), indicating that overall impact on Wikipedia traffic is moderate. Median effects cluster near zero, suggesting campaigns do not drastically alter total usage. However, <strong>community-driven initiatives like Wikipedia Asian Month show relatively stronger positive engagement signals</strong> compared to fundraising or photography campaigns. Campaigns have limited direct impact on overall pageview volume, as most of them, especially fundraising ones, target existing users and prioritize conversion over traffic growth, reflecting a different product objective rather than a lack of effectiveness.
                        </p>
                        <h3>4. Topic-Based Seasonal Behavior</h3>
                        <p>
                            Different content domains on Wikipedia exhibit distinct seasonal patterns. Education-related content follows strong academic cycles, political content shows moderate variation linked to real-world events, while entertainment remains relatively stable with weaker seasonality. This highlights a dual role of Wikipedia: it functions as a <strong>structured academic reference driven by school and work cycles</strong>, while also serving as a <strong>steady source of general and event-driven information</strong>. These patterns indicate that user intent varies by domain, and growth in one category is unlikely to cannibalize others, suggesting opportunities for cross-domain engagement.
                        </p>
            </div>
            <div class="footer">Interactive dashboard powered by Tableau Public</div>
        `,
        callback: () => {
            var divElement = document.getElementById('viz1773934367186');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    },
    "Reddit sentiment analysis": {
        title: "Reddit Sentiment Analysis",
        subtitle: "Interactive Tableau Dashboard for regional and platform-level insights",
        html: `
            <div class="dashboard-container">
                <div class='tableauPlaceholder' id='viz1773927011080' style='position: relative'><noscript><a href='#'><img alt='Reddit Dash ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Re&#47;Reddit_Dashboard&#47;RedditDash&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Reddit_Dashboard&#47;RedditDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Re&#47;Reddit_Dashboard&#47;RedditDash&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1773927011080');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1827px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
            </div>
            <div class="wiki-box insights-section">
                <h2>Data Insights & Analysis</h2>
                
                <div class="insight-item">
                    <h3>1. Post Volume Surge (Pre vs. Post ChatGPT)</h3>
                    <p>The launch of ChatGPT triggered a massive surge in discussions across AI and tech-related subreddits. Subreddits like <strong>r/singularity</strong>, <strong>r/technology</strong>, and <strong>r/wikipedia</strong> saw exponential growth in activity post-launch discussing the impact of AI on wikipedia, indicating a transformative shift in public interest toward generative AI.</p>
                </div>

                <div class="insight-item">
                    <h3>2. Sentiment Volatility & Trends</h3>
                    <p>While discussion volume increased, the average sentiment (Roberta Continuous) exhibited significant volatility. A noticeable dip in sentiment scores occurred immediately following the ChatGPT launch, suggesting that the massive influx of new users and broader public debate brought about more critical, cautious, or polarized perspectives on AI and Wikipedia compared to the earlier, more specialized discourse.</p>
                </div>

                <div class="insight-item">
                    <h3>3. Subreddit-Specific Sentiment</h3>
                    <ul>
                        <li><strong>Specialized Communities:</strong> Subreddits like <em>r/MachineLearning</em> and <em>r/artificial</em> maintain a generally positive or neutral outlook, focused on technical progress.</li>
                        <li><strong>General Tech Communities:</strong> <em>r/technology</em> and <em>r/wikipedia</em> exhibit more negative average sentiment, likely reflecting broader societal concerns regarding ethics, misinformation, LLM hallucinations and AI "hype."</li>
                    </ul>
                </div>

                <div class="insight-item">
                    <h3>4. Model Comparison: ROBERTA vs. VADER</h3>
                    <p>The sentiment classification analysis reveals that while both models agree on <strong>Neutral</strong> sentiment (high correlation), the <strong>ROBERTA</strong> transformer model provides more nuanced detection of negative sentiment compared to the lexicon-based <strong>VADER</strong>. Discrepancies often occur in complex social media text where sarcasm or technical context is present, highlighting ROBERTA's superior performance for this dataset.</p>
                    <p>This was done just to test how VADER and ROBERTA models worked and how they differed from each other.</p>
                </div>
            </div>
            <div class="footer">Interactive dashboard powered by Tableau Public</div>
        `,
        callback: () => {
            var divElement = document.getElementById('viz1773927011080');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    },
    "Twitter sentiment analysis": {
        title: "Twitter / X Sentiment Analysis",
        subtitle: "Interactive Tableau Dashboard for platform-level sentiment and topic insights",
        html: `
        <div class="dashboard-container">
            <div class='tableauPlaceholder' id='viz1773932868779' style='position: relative'><noscript><a href='#'><img alt='Dashboard 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17739303447700&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Book1_17739303447700&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_17739303447700&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>
            <script type='text/javascript'>
                var divElement = document.getElementById('viz1773932868779');
                var vizElement = divElement.getElementsByTagName('object')[0];
                vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);
            </script>
        </div>
        <div class="wiki-box insights-section">
            <h2>Data Insights & Analysis</h2>
            <div class="insight-item">
                <p>
                    An analysis of 3,500 Wikipedia-related tweets collected between January 2020 and late 2024 reveals a discernible and statistically meaningful shift in public brand perception of Wikipedia — one that corresponds closely with the emergence of large language models, and most acutely with the launch of ChatGPT in November 2022. Prior to this period, monthly tweet volume remained relatively stable, averaging between 50 and 80 posts per month, reflecting a consistent but largely specialist discourse confined to communities already familiar with Wikipedia's role as a digital knowledge resource.
                </p>
                <p>
                    The November 2022 inflection point is unambiguous in the data. Monthly tweet volume surged to approximately 125 posts — nearly double the pre-launch average — and crucially, did not regress to prior levels in subsequent months. This sustained elevation indicates that ChatGPT's introduction did not merely generate a transient spike in public curiosity, but fundamentally repositioned Wikipedia within broader public discourse. Where Wikipedia had previously occupied the role of an uncontested primary reference, the advent of generative AI introduced a comparative dimension to public conversation — one in which Wikipedia's credibility, accuracy, and editorial integrity were actively debated in relation to AI-generated outputs.
                </p>
                <p>
                    This structural shift is further corroborated by the sentiment composition data. The RoBERTa model — selected over VADER as the primary analytical instrument owing to its superior sensitivity to contextual nuance and negation — classifies 45.2% of all posts as positive, 30.0% as negative, and 24.8% as neutral across the full five-year period. However, a temporal disaggregation of these figures reveals a more complex trajectory. Pre-launch sentiment was characterised by a dominant positive composition, consistent with a period in which Wikipedia faced little direct reputational challenge. Post-launch, the neutral and negative proportions expanded measurably, reflecting the influx of comparative and evaluative discourse rather than straightforward reference or endorsement.
                </p>
                <p>
                    The monthly RoBERTa continuous sentiment score substantiates this interpretation. Scores fluctuated within a broadly positive range of 0.0 to +0.3 throughout the pre-ChatGPT period, with limited volatility. Following the launch, the score exhibited markedly greater oscillation, with more frequent and deeper dips into negative territory observed through 2023 and into 2024. Notably, however, the sentiment baseline did not sustain a negative trajectory — scores recovered consistently following each trough, suggesting that Wikipedia's brand equity on the platform remained fundamentally resilient despite the intensification of critical discourse.
                </p>
                <p>
                    Taken together, these findings support a nuanced conclusion: the introduction of ChatGPT did not erode Wikipedia's brand perception on Twitter, but it materially altered its character. Public engagement shifted from passive endorsement to active scrutiny — a transition that, while introducing greater sentiment volatility, simultaneously affirmed Wikipedia's continuing relevance as an epistemic benchmark in the age of artificial intelligence. The data indicates that Twitter users increasingly positioned Wikipedia not as a relic of the pre-AI information landscape, but as the human-verified standard against which machine-generated knowledge is evaluated and challenged.
                </p>
            </div>
        </div>
        <div class="footer">Interactive dashboard powered by Tableau Public</div>
    `,
        callback: () => {
            var divElement = document.getElementById('viz1773932868779');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    },
    "editorAnalysis": {
        title: "Wikipedia Editor Analysis (2001–2026)",
        subtitle: "Community health trends, growth rates, and seasonal patterns",
        html: `
            <div class="dashboard-container">
                <div class='tableauPlaceholder' id='vizEditorAnalysis' style='position: relative'>
                    <noscript>
                        <a href='#'><img alt='Editor Analysis' src='https://public.tableau.com/static/images/Ed/EditorAnalysis/EditorAnalysisDashboard/1.png' style='border: none' /></a>
                    </noscript>
                    <object class='tableauViz' style='display:none;'>
                        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                        <param name='embed_code_version' value='3' />
                        <param name='site_root' value='' />
                        <param name='name' value='EditorAnalysis/EditorAnalysisDashboard' />
                        <param name='tabs' value='yes' />
                        <param name='toolbar' value='yes' />
                        <param name='animate_transition' value='yes' />
                        <param name='display_static_image' value='yes' />
                        <param name='display_spinner' value='yes' />
                        <param name='display_overlay' value='yes' />
                        <param name='display_count' value='yes' />
                        <param name='language' value='en-US' />
                    </object>
                </div>
            </div>
            <div class="wiki-box insights-section">
                <h2>Data Insights & Analysis</h2>
                <div class="insight-item">
                    <h3>1. Editor Community Trends</h3>
                    <p>Wikipedia's active editor count reflects the platform's evolution from niche encyclopedia to global knowledge commons. Early growth (2001–2007) saw rapid adoption, peaking at ~63,000 editors in March 2007. Subsequent years show stabilization around 40,000 editors, with seasonal variations linked to academic calendars and engagement campaigns.</p>
                </div>
                <div class="insight-item">
                    <h3>2. Seasonality & Engagement Patterns</h3>
                    <p>Editor activity exhibits strong monthly seasonality, with predictable peaks during school/work calendar periods and troughs during summer months. This reveals that Wikipedia editing is integrated into academic and professional workflows, rather than casual leisure activity.</p>
                </div>
                <div class="insight-item">
                    <h3>3. Growth Rate Analysis</h3>
                    <p>Month-over-month and year-over-year growth analysis shows stabilization post-2007, with minimal sustained growth. This indicates market saturation among active editors, suggesting future growth requires strategies focused on editor retention and community health rather than raw acquisition.</p>
                </div>
                <div class="insight-item">
                    <h3>4. Community Health Metrics</h3>
                    <p>Rolling volatility analysis identifies periods of community flux. Anomaly detection reveals significant shifts corresponding to platform changes, policy updates, and external events that impact editor engagement and retention.</p>
                </div>
            </div>
            <div class="footer">Interactive dashboard powered by Tableau Public</div>
        `,
        callback: () => {
            var divElement = document.getElementById('vizEditorAnalysis');
            var vizElement = divElement.getElementsByTagName('object')[0];

            if (divElement.offsetWidth > 800) {
                vizElement.style.width = '100%';
                vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            } else if (divElement.offsetWidth > 500) {
                vizElement.style.width = '100%';
                vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            } else {
                vizElement.style.width = '100%';
                vizElement.style.height = '1400px';
            }

            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    },
    "strategic_insights": {
        title: "Integrated Business Insights & Strategic Recommendations",
        subtitle: "From Wikipedia, the free product analysis",
        html: `
            <div class="wiki-box" style="border-left: none; background: none; border: 1px solid #a2a9b1; padding: 1em; margin-bottom: 2em; font-size: 0.9em;">
                <p><strong>Combined synthesis</strong> of findings across pageview trends, community sentiment, and user behavior analysis (2015–2025).</p>
            </div>

            <h2>Cross-Sectional Findings <a class="edit-link">edit</a></h2>
            
            <h3>Convergent Evidence Across All Data Sources <a class="edit-link">edit</a></h3>
            <p>
                The four analytical perspectives—<a class="wiki-link">pageview analysis</a>, <a class="wiki-link">Reddit sentiment</a>, user survey, and <a class="wiki-link">graph analytics</a>—produce a coherent and mutually reinforcing picture. Wikipedia’s aggregate traffic has declined since 2023, Reddit sentiment toward AI and Wikipedia has become measurably more negative since <a class="wiki-link">ChatGPT</a>’s launch, and survey respondents confirm active substitution of Wikipedia with AI tools as their primary daily information source.
            </p>
            <p>
                At the same time, all sources identify Wikipedia’s enduring competitive advantage: <strong>trust</strong>. Survey respondents trust Wikipedia more than AI tools despite using it less. Reddit users route to Wikipedia specifically to verify AI claims, and this behaviour is growing. The strategic opportunity is to close the usability gap without compromising the editorial integrity that creates the trust advantage in the first place.
            </p>

            <h3>The Trust-Usage Paradox <a class="edit-link">edit</a></h3>
            <p>
                The most important quantitative finding is the persistent gap between stated trust and observed usage. Wikipedia commands higher trust ratings than AI tools from a plurality of student respondents, yet AI tools have captured daily usage frequency across every access band. This paradox has a single root cause: the article format was designed for exploratory desktop reading, and the dominant use case in 2026 is mobile, goal-directed, and time-constrained.
            </p>

            <h2>Strategic Recommendations <a class="edit-link">edit</a></h2>

            <h3>Rec 1: Deploy AI Summaries <a class="edit-link">edit</a></h3>
            <p>
                Across the survey’s feature wishlist, format preference, and frustration analysis, a single feature emerges as both the most requested and the most likely to re-engage lapsed users: an <strong>AI-generated summary</strong> positioned at the top of each Wikipedia article. Demand is concentrated in the largest frustration segments—users frustrated by excessive length and lack of direct answers.
            </p>

            <h3>Rec 2: Formalise the AI Verification Layer <a class="edit-link">edit</a></h3>
            <p>
                Reddit analysis shows that users already treat Wikipedia as the corrective tool for AI inaccuracies. The <a class="wiki-link">Wikimedia Foundation</a> <a class="lang-code">de</a> should formalise this role by negotiating structured data agreements with major AI providers requiring visible attribution whenever factual claims are grounded in Wikipedia content.
            </p>

            <h3>Rec 3: Launch a Simplified Student Mode <a class="edit-link">edit</a></h3>
            <p>
                The survey’s top feature wishlist item is a simplified student mode—a dedicated interface with jargon-reduced language, structured summaries, and curriculum-aligned framing. Given that the overwhelming majority of respondents are students aged 17–22, this mode would serve the modal user rather than a niche segment.
            </p>

            <h3>Rec 4: Invest in the Mobile App <a class="edit-link">edit</a></h3>
            <p>
                Mobile app traffic is 28% less volatile, has stronger autocorrelation, and recovers from disruption 1.8× faster than web traffic. The app channel also shows the highest <a class="wiki-link">CAGR</a> among all three platforms. These properties make the mobile app the most strategically valuable surface for product innovation.
            </p>

            <h3>Rec 5: Protect Editorial Integrity <a class="edit-link">edit</a></h3>
            <p>
                Multiple signals point to a growing risk that AI-generated content is entering Wikipedia through editors who paste AI output without adequate verification. Wikipedia’s entire value proposition rests on being the source humans trust over AI.
            </p>

            <div class="wiki-box" style="border-left: none; margin-top: 3rem; padding: 0;">
                <h2 style="border-bottom: 2px solid #202122;">Conclusion <a class="edit-link">edit</a></h2>
                <p>
                    Wikipedia remains a <strong>trusted and resilient knowledge platform</strong>, but its usage is evolving. While AI tools are increasingly used for quick, everyday queries, Wikipedia continues to play a key role in <strong>verification and reliable information access</strong>. The data highlights a <strong>gap between trust and usage</strong>, along with opportunities across time (weekends, seasonal dips) and content formats where engagement can be improved. Moving forward, the focus should be on making trusted knowledge easier and faster to access, especially in mobile and time-constrained contexts, while <strong>preserving the human-driven editorial process that underpins its credibility</strong>.
                </p>
     </div>
        `
    },

};

function renderContent(key) {
    const data = contentData[key];
    const header = document.querySelector('header');
    const container = document.getElementById('main-container');

    // Update Header
    header.innerHTML = `
        <h1>${data.title}</h1>
        <div class="subtitle">${data.subtitle}</div>
    `;

    // Update Content
    container.innerHTML = data.html;

    // Run Callback if exists
    if (data.callback) {
        data.callback();
    }

    // Update Sidebar Active State
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-tab') === key) {
            item.classList.add('active');
        }
    });

    // Scroll to top
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial Render
    renderContent('home');

    // Event Listeners for Sidebar
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', (e) => {
            const key = e.target.getAttribute('data-tab');
            if (key) {
                renderContent(key);
            }
        });
    });
});

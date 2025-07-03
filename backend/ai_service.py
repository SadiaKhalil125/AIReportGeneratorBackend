import openai
import os

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.openai_api_key:
            try:
                self.client = openai.OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                print("Falling back to demo content generation")
                self.client = None
    
    async def generate_report_content(self, topic: str) -> str:
        """Generate detailed report content for the given topic"""
        
        if self.openai_api_key:
            try:
                return await self._generate_with_openai(topic)
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._generate_demo_content(topic)
        else:
            return self._generate_demo_content(topic)
    
    async def _generate_with_openai(self, topic: str) -> str:
        """Generate content using OpenAI API"""
        
        if not self.client:
            return self._generate_demo_content(topic)
        
        prompt = f"""
        Create a comprehensive, detailed research report on the topic: "{topic}"
        
        The report should include:
        1. Executive Summary
        2. Introduction and Background
        3. Current State Analysis
        4. Key Findings and Insights
        5. Challenges and Opportunities
        6. Future Trends and Predictions
        7. Recommendations
        8. Conclusion
        
        Make the report professional, well-structured, and informative.
        Use clear headings for each section (end each heading with a colon).
        Provide detailed explanations and analysis.
        The report should be suitable for business or academic purposes.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional research analyst creating detailed reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else self._generate_demo_content(topic)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._generate_demo_content(topic)
    
    def _generate_demo_content(self, topic: str) -> str:
        """Generate demo content when OpenAI is not available"""
        
        return f"""Executive Summary:
This comprehensive report examines {topic} from multiple perspectives, providing insights into current trends, challenges, and future opportunities. Our analysis reveals significant developments in this field that warrant attention from stakeholders and decision-makers.

Introduction and Background:
{topic} has emerged as a critical area of focus in today's rapidly evolving landscape. Understanding its implications requires a thorough examination of historical context, current applications, and future potential. This report aims to provide a detailed analysis that can inform strategic decision-making.

Current State Analysis:
The current state of {topic} is characterized by rapid growth and innovation. Key players in the market are investing heavily in research and development, leading to breakthrough technologies and methodologies. Market adoption rates have shown consistent upward trends, indicating strong demand and acceptance.

Key market indicators include:
• Increased investment from venture capital and institutional investors
• Growing number of specialized companies and startups
• Expansion of use cases across various industries
• Enhanced regulatory frameworks and standards

Key Findings and Insights:
Our research has identified several critical findings regarding {topic}:

1. Market Growth: The sector has experienced unprecedented growth rates, with projections indicating continued expansion over the next five years.

2. Technology Advancement: Significant technological breakthroughs have improved efficiency, accuracy, and accessibility.

3. Industry Adoption: Major corporations across various sectors are implementing solutions related to {topic}, driving mainstream acceptance.

4. Consumer Behavior: End-user preferences and behaviors are evolving, creating new opportunities for innovation and service delivery.

Challenges and Opportunities:
While {topic} presents numerous opportunities, several challenges must be addressed:

Challenges:
• Regulatory uncertainty in some jurisdictions
• Skills gap in the workforce
• Infrastructure limitations
• Privacy and security concerns
• Cost barriers for smaller organizations

Opportunities:
• Emerging markets showing high growth potential
• Cross-industry collaboration possibilities
• Innovation in supporting technologies
• Government initiatives and funding programs
• Increasing consumer awareness and demand

Future Trends and Predictions:
Based on current trajectories and expert analysis, we anticipate several key trends in {topic}:

1. Increased Automation: Greater integration of automated systems and processes
2. Enhanced User Experience: Focus on intuitive interfaces and user-centric design
3. Sustainability Integration: Growing emphasis on environmental and social responsibility
4. Global Standardization: Development of universal standards and protocols
5. Democratization: Increased accessibility for smaller organizations and individuals

Recommendations:
Based on our analysis, we recommend the following strategic actions:

1. Investment Strategy: Organizations should consider strategic investments in {topic} to maintain competitive advantage.

2. Skill Development: Invest in training and development programs to build internal capabilities.

3. Partnership Opportunities: Explore collaborative partnerships with technology providers and industry leaders.

4. Risk Management: Develop comprehensive risk assessment and mitigation strategies.

5. Regulatory Compliance: Stay informed about evolving regulations and ensure compliance frameworks are in place.

Conclusion:
{topic} represents a significant opportunity for organizations willing to embrace innovation and adapt to changing market conditions. While challenges exist, the potential benefits far outweigh the risks for those who approach implementation strategically.

Success in this domain requires a balanced approach that considers technological capabilities, market dynamics, regulatory requirements, and organizational readiness. Organizations that act decisively while maintaining flexibility will be best positioned to capitalize on the opportunities presented by {topic}.

The landscape will continue to evolve rapidly, making it essential for stakeholders to remain informed and agile in their approach. Regular reassessment of strategies and objectives will be crucial for long-term success in this dynamic environment.""" 
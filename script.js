// Static charity list with name, description, and donation link
const charityList = [
  {
    charity: "Embrace the Middle East",
    description: "This charity works to support marginalized and vulnerable communities across the Middle East, providing humanitarian aid, education, and healthcare. Their projects focus on long-term solutions to poverty and injustice, empowering local communities through sustainable programs. With an ecumenical Christian foundation, they partner with local organizations to promote dignity and hope.",
    donationLink: "https://embraceme.org/donate"
  },
  {
    charity: "Alliance for Middle East Peace (ALLMEP)",
    description: "ALLMEP is a coalition of over 160 organizations dedicated to peacebuilding between Israelis and Palestinians. By supporting grassroots initiatives, they promote dialogue, cooperation, and mutual understanding to build a more peaceful future. They also advocate for international support to expand their conflict-resolution efforts.",
    donationLink: "https://www.allmep.org/donate/"
  },
  {
    charity: "American Near East Refugee Aid (Anera)",
    description: "Anera delivers vital programs to alleviate poverty and suffering in the Middle East, focusing on education, health, and economic development. They provide medical aid, vocational training, and emergency relief to communities affected by conflict. Their initiatives create sustainable opportunities, particularly for refugees and vulnerable populations.",
    donationLink: "https://www.anera.org/donate/"
  },
  {
    charity: "Disasters Emergency Committee (DEC) – Middle East Humanitarian Appeal",
    description: "DEC coordinates emergency relief efforts for humanitarian crises in Gaza, Lebanon, and the West Bank. Their aid includes food, clean water, and medical assistance to communities impacted by conflict and displacement. They bring together multiple charities to ensure rapid and effective disaster response.",
    donationLink: "https://www.dec.org.uk/appeal/middle-east-humanitarian-appeal"
  },
  {
    charity: "Bill & Melinda Gates foundation – Middle East Initiatives",
    description: "This foundation partners with organizations in the Middle East to address critical issues such as healthcare, poverty, and agricultural development. Their initiatives focus on reducing preventable diseases, improving education, and fostering economic growth. By funding innovative solutions, they aim to create lasting change in struggling communities.",
    donationLink: "https://www.gatesfoundation.org/"
  },
  {
    charity: "World Food Programme (WFP)",
    description: "WFP provides food assistance to vulnerable populations across the Middle East, tackling hunger and malnutrition. Their programs deliver emergency food supplies while also supporting sustainable solutions for food security. Through partnerships with local governments and organizations, they help communities build resilience against food crises.",
    donationLink: "https://www.wfp.org/donate"
  },
  {
    charity: "UNICEF",
    description: "UNICEF works to protect children across the Middle East by providing education, healthcare, and humanitarian aid. Their programs focus on immunizations, clean water, nutrition, and emergency relief for children affected by war and poverty. They advocate for children's rights and ensure access to essential services in crisis-affected regions.",
    donationLink: "https://www.unicef.org/"
  },
  {
    charity: "CARE",
    description: "CARE delivers both immediate relief and long-term development programs in the Middle East, focusing on food security, education, and women's empowerment. Their work helps families rebuild their lives after conflict and displacement. They also provide economic opportunities for women to support self-sufficiency and social stability.",
    donationLink: "https://www.care.org/"
  },
  {
    charity: "Islamic Relief USA",
    description: "Islamic Relief USA provides comprehensive humanitarian aid across the Middle East, including emergency relief, healthcare, clean water, and education. Their projects focus on both immediate assistance and long-term development, helping communities recover from crises. They also support livelihood programs to foster self-reliance.",
    donationLink: "https://irusa.org/middle-east/"
  },
  {
    charity: "Middle East Children's Alliance (MECA)",
    description: "MECA delivers medical aid and supports community projects that improve the lives of Palestinian children and refugees from Syria. Their work includes providing educational resources, clean water initiatives, and trauma relief programs. They focus on empowering children and families to rebuild their futures.",
    donationLink: "https://www.mecaforpeace.org/"
  },
  {
    charity: "Palestine Children's Relief Fund (PCRF)",
    description: "PCRF provides life-saving medical care to children in the Middle East, including those in the West Bank and Gaza. They arrange free surgeries and medical treatments for children in need, regardless of nationality or religion. Their long-term projects include building pediatric cancer centers to improve healthcare access.",
    donationLink: "https://www.pcrf.net/"
  },
  {
    charity: "United Nations Relief and Works Agency for Palestine Refugees (UNRWA)",
    description: "UNRWA provides essential services such as food, education, and healthcare to Palestinian refugees across the Middle East. They support millions of people in Gaza, the West Bank, Lebanon, Syria, and Jordan. Their work ensures that displaced communities have access to basic human rights and opportunities for a better future.",
    donationLink: "https://donate.unrwa.org/int/en/general"
  },
  {
    charity: "Project HOPE",
    description: "Project HOPE strengthens health systems and provides emergency medical aid in the Middle East and North Africa. Their work includes training healthcare workers, delivering life-saving medicines, and responding to humanitarian crises. They focus on long-term health solutions to build stronger communities.",
    donationLink: "https://www.projecthope.org/region/middle-east-north-africa/"
  },
  {
    charity: "Médecins Sans Frontières (Doctors Without Borders)",
    description: "Doctors Without Borders provides emergency medical care in conflict zones across the Middle East, including Syria, Yemen, and Iraq. Their teams offer surgical care, maternal health services, and treatment for malnutrition and disease outbreaks. They operate independently, ensuring aid reaches those most in need.",
    donationLink: "https://www.msf.org/donate"
  },
  {
    charity: "International Rescue Committee (IRC)",
    description: "IRC provides life-saving healthcare, child protection, and emergency relief to people affected by war and displacement in the Middle East. Their programs help rebuild communities by offering job training, education, and economic support. They focus on both immediate humanitarian assistance and long-term stability.",
    donationLink: "https://www.rescue.org/donate"
  },
  {
    charity: "Save the Children",
    description: "Save the Children delivers education, healthcare, and emergency relief to children affected by conflict in the Middle East. Their programs focus on ensuring access to learning, nutrition, and psychological support for children in crisis. They advocate for children's rights and work to create a brighter future for vulnerable youth.",
    donationLink: "https://www.savethechildren.org/us/what-we-do/where-we-work/greater-middle-east-eurasia"
  },
  {
    charity: "Action Against Hunger",
    description: "Action Against Hunger combats food insecurity and malnutrition in the Middle East by providing emergency food aid and sustainable farming solutions. Their projects include distributing food parcels and supporting communities in developing long-term food production. They focus on addressing the root causes of hunger and building resilience.",
    donationLink: "https://www.actionagainsthunger.org/donate"
  }
];

// Wait until the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  const submitBtn  = document.getElementById('submit-btn');
  const resultsBox = document.getElementById('results-container');
  const resultText  = document.getElementById('result-text');

  const getRadio = n =>
    (document.querySelector(`input[name="${n}"]:checked`) || {}).value || null;

  const getChecks = n =>
    Array.from(document.querySelectorAll(`input[name="${n}"]:checked`))
         .map(el => el.value);

  submitBtn.addEventListener('click', () => {
    const answers = {
      cause:   getRadio('cause'),
      groups:  getChecks('groups'),
      region:  getRadio('region'),
      faith:   getRadio('faith'),
      support: getRadio('support')
    };

    // Show results container
    resultsBox.style.display = 'block';

    // Send answers to the backend API
    fetch('/api/charity-match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    })
      .then(r => { 
        if (!r.ok) throw new Error(r.statusText); 
        return r.json(); 
      })
      .then(data => {
        console.log("API Response:", data); // Log the full API response for debugging

        // Check if the response has the expected structure
        if (data && data.choices && data.choices.length > 0) {
          const aiResult = data.choices[0].message.content;
          console.log("AI Result:", aiResult); // Log the raw result from the AI

          // Extract charity name, description, and donation link
          const charityMatch = aiResult.match(/\*\*(.*?)\*\*/); // Match bolded charity name
          const descriptionMatch = aiResult.match(/- \*\*Description\*\*:(.*?)\n/);  // Match description
          const donationLinkMatch = aiResult.match(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/); // Match donation link

          if (charityMatch && descriptionMatch && donationLinkMatch) {
            const charity = charityMatch[1];
            const description = descriptionMatch[1].trim();
            const donationLink = donationLinkMatch[2];

            // Dynamically display the result from the API
            resultText.innerHTML = `
              <strong>${charity}</strong><br />
              <p>${description}</p>
              <a href="${donationLink}" target="_blank">Donate to ${charity}</a>
            `;
          } else {
            console.error("Error extracting data from AI response.");
            resultText.innerHTML = '⚠️ Unable to parse AI response properly.';
          }
        } else {
          console.error("No valid data received from backend.");
          resultText.innerHTML = '⚠️ No charity match found or invalid data received.';
        }

        // Display the static charity list under the result
        const staticCharityListHTML = charityList.map(charity => `
          <div class="charity-result">
            <strong>${charity.charity}</strong><br />
            <p>${charity.description}</p>
            <a href="${charity.donationLink}" target="_blank">Donate to ${charity.charity}</a>
          </div>
        `).join('');

        // Append the static charity list below the result
        resultText.innerHTML += `
          <h3>Other Charities You Can Support:</h3>
          ${staticCharityListHTML}
        `;

        resultsBox.style.display = 'block'; // Ensure the results box is visible
      })
      .catch(err => {
        console.error(err);
        resultText.innerHTML = '⚠️ Error calling backend.';
        resultsBox.style.display = 'block';
      });
  });
});

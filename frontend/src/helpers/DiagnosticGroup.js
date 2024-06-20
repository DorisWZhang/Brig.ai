export const DiagnosticGroups = [
    {   
      ID: "PCOS Cluster 0",
      message: "Based on your self reported symptoms, currently we do not recommend any specific diagnostic tests. If you strongly believe there is an issue, we suggest that you consult another professional opinion, such as an OB-GYN, family doctor, or endocrinologist.",
      tests: []
    },
    {   
      ID: "PCOS Cluster 1",
      message: "Your results show a moderate severity of PCOS symptoms, including significant hormonal imbalances and menstrual irregularities.",
      tests: [
        {
          name: "Pelvic Ultrasound",
          explanation: "To take images of the reproductive organs and look for endometrial implants or cysts. A transducer device is used either externally on the abdomen or internally."
        },
        {
          name: "Hormonal Panel",
          explanation: "Examining testosterone, LH, FSH, and prolactin levels to check for hormonal imbalances."
        },
        {
          name: "Glucose Tolerance Test",
          explanation: "To check for insulin resistance, common in PCOS."
        }
      ]
    },
    {   
      ID: "PCOS Cluster 2",
      message: "Your results show a high severity of PCOS symptoms, including significant hormonal imbalances and menstrual irregularities.",
      tests: [
        {
          name: "Pelvic Ultrasound",
          explanation: "To take images of the reproductive organs and look for endometrial implants or cysts. A transducer device is used either externally on the abdomen or internally."
        },
        {
          name: "Advanced Hormonal Testing",
          explanation: "Examining testosterone, LH, FSH, androgen levels, anti-Müllerian hormone (AMH), and prolactin levels to check for hormonal imbalances."
        },
        {
          name: "MRI (Magnetic Resonance Imaging)",
          explanation: "To provide detailed images of the pelvic area and identify endometrial implants or cysts. Non-invasive magnetic fields and radio waves create detailed 3D images."
        },
        {
          name: "Laparoscopy",
          explanation: "The gold standard for diagnosing endometriosis. A surgical procedure where a camera (laparoscope) is inserted through a small incision in the abdomen to examine the pelvic organs."
        }
      ]
    },
    {   
      ID: "PCOS Cluster 3",
      message: "Your results show mixed PCOS symptoms with gastrointestinal issues.",
      tests: [
        {
          name: "Gastrointestinal Testing",
          explanation: "To check for gastrointestinal issues that may be contributing to your symptoms. This may include tests for food intolerances, celiac disease, or other gastrointestinal disorders."
        },
        {
          name: "Pelvic Ultrasound",
          explanation: "To take images of the reproductive organs and look for endometrial implants or cysts. A transducer device is used either externally on the abdomen or internally."
        },
        {
          name: "Advanced Hormonal Testing",
          explanation: "Examining testosterone, LH, FSH, androgen levels, anti-Müllerian hormone (AMH), and prolactin levels to check for hormonal imbalances."
        },
        {
          name: "MRI (Magnetic Resonance Imaging)",
          explanation: "To provide detailed images of the pelvic area and identify endometrial implants or cysts. Non-invasive magnetic fields and radio waves create detailed 3D images."
        },
        {
          name: "Laparoscopy",
          explanation: "The gold standard for diagnosing endometriosis. A surgical procedure where a camera (laparoscope) is inserted through a small incision in the abdomen to examine the pelvic organs."
        }
      ]
    },
    {   
      ID: "Endo Cluster 0",
      message: "Based on your self reported symptoms, currently we do not recommend any specific diagnostic tests. If you strongly believe there is an issue, we suggest that you consult another professional opinion, such as an OB-GYN, family doctor, or endocrinologist.",
      tests: []
    },
    {   
      ID: "Endo Cluster 1",
      message: "Your results show a moderate severity of endometriosis symptoms, including significant pelvic pain and menstrual irregularities.",
      tests: [
        {
          name: "Pelvic Exam",
          explanation: "A healthcare provider manually examines the pelvis to feel for any abnormalities such as cysts or scars behind the uterus, which may be indicative of endometriosis."
        },
        {
          name: "Pelvic Ultrasound",
          explanation: "To take images of the reproductive organs and look for endometrial implants or cysts. A transducer device is used either externally on the abdomen or internally."
        },
        {
          name: "MRI (Magnetic Resonance Imaging)",
          explanation: "To provide detailed images of the pelvic area and identify endometrial implants or cysts. Non-invasive magnetic fields and radio waves create detailed 3D images."
        },
        {
          name: "Laparoscopy",
          explanation: "The gold standard for diagnosing endometriosis. A surgical procedure where a camera (laparoscope) is inserted through a small incision in the abdomen to examine the pelvic organs."
        }
      ]
    }
  ];
  
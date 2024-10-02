import os

from groq import Groq

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
  {
    "role": "system",
    "content": "You are a SQL expert. Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. \n===Tables \n\n         CREATE TABLE payment (\n    payment_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,\n    customer_id SMALLINT UNSIGNED NOT NULL,\n    staff_id TINYINT UNSIGNED NOT NULL,\n    rental_id INT NULL,\n    amount DECIMAL(5,2) NOT NULL,\n    payment_date DATETIME NOT NULL,\n    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n    PRIMARY KEY (payment_id),\n    KEY customer_id (customer_id),\n    KEY staff_id (staff_id),\n    KEY rental_id (rental_id)\n);\n\n\n\n\n         CREATE TABLE payment (\n            payment_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,\n            customer_id SMALLINT UNSIGNED NOT NULL,\n            staff_id TINYINT UNSIGNED NOT NULL,\n            rental_id INT NULL,\n            amount DECIMAL(5,2) NOT NULL,\n            payment_date DATETIME NOT NULL,\n            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n            PRIMARY KEY (payment_id),\n            KEY customer_id (customer_id),\n            KEY staff_id (staff_id),\n            KEY rental_id (rental_id)\n        );\n\n\n\n     CREATE TABLE `payment` (\n  `payment_id` smallint unsigned NOT NULL AUTO_INCREMENT,\n  `customer_id` smallint unsigned NOT NULL,\n  `staff_id` tinyint unsigned NOT NULL,\n  `rental_id` int DEFAULT NULL,\n  `amount` decimal(5,2) NOT NULL,\n  `payment_date` datetime NOT NULL,\n  `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n  PRIMARY KEY (`payment_id`),\n  KEY `idx_fk_staff_id` (`staff_id`),\n  KEY `idx_fk_customer_id` (`customer_id`),\n  KEY `fk_payment_rental` (`rental_id`),\n  CONSTRAINT `fk_payment_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,\n  CONSTRAINT `fk_payment_rental` FOREIGN KEY (`rental_id`) REFERENCES `rental` (`rental_id`) ON DELETE SET NULL ON UPDATE CASCADE,\n  CONSTRAINT `fk_payment_staff` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE\n) \n\n\n===Response Guidelines \n1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. \n2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n3. If the provided context is insufficient, please explain why it can't be generated. \n4. Please use the most relevant table(s). \n5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n6. Ensure that the output SQL is SQL-compliant and executable, and free of syntax errors. \n"
  },
  {
    "role": "user",
    "content": "what is the  average amount"
  }
],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
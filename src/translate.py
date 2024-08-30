import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=key)

def translate_system_prompt(conversations):
    return [
        {
            **conv,
            'value': conv['value'].replace(
                "You are a helpful assistant that answers in JSON. Here's the json schema you must adhere to:",
                "Anda adalah asisten yang membantu menjawab dalam format JSON. Berikut skema JSON yang harus Anda ikuti:"
            ) if conv['from'] == 'system' else conv['value']
        }
        for conv in conversations
    ]

def translate_user_prompt_(query):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Anda adalah ahli bahasa Indonesia yang menerjemahkan teks dari bahasa Inggris ke bahasa Indonesia. Anda tidak perlu menerjemahkan teks yang merupakan istilah yang biasanya diapit oleh tanda petik ganda"},
            {"role": "user", "content": "Terjemahkan instruksi berikut:\n" + query},
        ]
    )
    return response.choices[0].message.content

def translate_user_prompt(conversations):
    for conv in conversations:
        if conv['from'] == 'human':
            conv['value'] = translate_user_prompt_(conv['value'])  # Translate using the provided function
    return conversations

CATEGORIES = {
    "Materials": "Bahan",
    "Financial Services (New Name)": "Layanan Keuangan",
    "Consumer Discretionary Distribution & Retail (New Name)": "Distribusi & Ritel Konsumen Discretionary",
    "Capital Goods": "Barang Modal",
    "Transportation": "Transportasi",
    "Consumer Durables & Apparel": "Konsumen Tahan Lama & Pakaian",
    "Commercial & Professional Services": "Layanan Komersial & Profesional",
    "Energy": "Energi",
    "Health Care Equipment & Services": "Peralatan & Layanan Kesehatan",
    "Food, Beverage & Tobacco": "Makanan, Minuman & Tembakau",
    "Consumer Services": "Layanan Konsumen",
    "Technology Hardware & Equipment": "Perangkat Keras & Peralatan Teknologi",
    "Software & Services": "Perangkat Lunak & Layanan",
    "Insurance": "Asuransi",
    "Consumer Staples Distribution & Retail (New Name)": "Distribusi & Ritel Barang Konsumen",
    "Automobiles & Components": "Otomotif & Komponen",
    "Pharmaceuticals, Biotechnology & Life Sciences": "Farmasi, Bioteknologi & Ilmu Kehidupan",
    "Banks": "Bank",
    "Media & Entertainment": "Media & Hiburan",
    "Telecommunication Services": "Layanan Telekomunikasi",
    "JSON Schema": "Skema JSON",
    "Semiconductors & Semiconductor Equipment": "Semikonduktor & Peralatan Semikonduktor",
    "Household & Personal Products": "Produk Rumah Tangga & Pribadi"
}

SUBCATEGORIES = {
    "Metals & Mining": "Logam & Pertambangan",
    "Specialty Retail": "Ritel Khusus",
    "Commercial Services & Supplies": "Layanan & Persediaan Komersial",
    "Financial Services (New Name)": "Layanan Keuangan",
    "Household Durables": "Barang Tahan Lama Rumah Tangga",
    "Chemicals": "Bahan Kimia",
    "Oil, Gas & Consumable Fuels": "Minyak, Gas & Bahan Bakar Konsumsi",
    "Health Care Providers & Services": "Penyedia & Layanan Kesehatan",
    "Ground Transportation (New Name)": "Transportasi Darat",
    "Hotels, Restaurants & Leisure": "Hotel, Restoran & Rekreasi",
    "Consumer Staples Distribution & Retail (New Name)": "Distribusi & Ritel Barang Konsumen",
    "Insurance": "Asuransi",
    "Capital Markets": "Pasar Modal",
    "Electronic Equipment, Instruments & Components": "Peralatan Elektronik, Instrumen & Komponen",
    "Textiles, Apparel & Luxury Goods": "Tekstil, Pakaian & Barang Mewah",
    "Professional Services": "Layanan Profesional",
    "Machinery": "Mesin",
    "Beverages": "Minuman",
    "Transportation Infrastructure": "Infrastruktur Transportasi",
    "IT Services": "Layanan TI",
    "Media": "Media",
    "Energy Equipment & Services": "Peralatan & Layanan Energi",
    "Broadline Retail (New Name)": "Ritel Umum",
    "Diversified Consumer Services": "Layanan Konsumen yang Diversifikasi",
    "Paper & Forest Products": "Kertas & Produk Hutan",
    "Food Products": "Produk Makanan",
    "Containers & Packaging": "Kontainer & Kemasan",
    "Software": "Perangkat Lunak",
    "Health Care Equipment & Supplies": "Peralatan & Persediaan Kesehatan",
    "Semiconductors & Semiconductor Equipment": "Semikonduktor & Peralatan Semikonduktor",
    "Automobiles": "Otomotif",
    "Electrical Equipment": "Peralatan Listrik",
    "Diversified Telecommunication Services": "Layanan Telekomunikasi yang Diversifikasi",
    "Automobile Components (New Name)": "Komponen Otomotif",
    "Banks": "Bank",
    "Healthcare System Schema": "Skema Sistem Kesehatan",
    "Consumer Finance": "Keuangan Konsumen",
    "Mortgage Real Estate Investment Trusts (REITs)": "REITs Investasi Properti Hipotek",
    "Technology Hardware, Storage & Peripherals": "Perangkat Keras Teknologi, Penyimpanan & Periferal",
    "Thrifts & Mortgage Finance (Discontinued)": "Tabungan & Keuangan Hipotek (Dihentikan)",
    "Distributors": "Distributor",
    "Internet & Direct Marketing Retail (Discontinued)": "Ritel Pemasaran Langsung & Internet (Dihentikan)",
    "Trading Companies & Distributors": "Perusahaan Perdagangan & Distributor",
    "Wireless Telecommunication Services": "Layanan Telekomunikasi Nirkabel",
    "Life Sciences Tools & Services": "Alat & Layanan Ilmu Kehidupan",
    "Pharmaceuticals": "Farmasi",
    "Aerospace & Defense": "Dirgantara & Pertahanan",
    "Industrial Conglomerates": "Konglomerat Industri",
    "Building Products": "Produk Konstruksi",
    "Biotechnology": "Bioteknologi",
    "Communications Equipment": "Peralatan Komunikasi",
    "Construction Materials": "Bahan Konstruksi",
    "Marine Transportation (New Name)": "Transportasi Laut",
    "Health Care Technology": "Teknologi Kesehatan",
    "Personal Care Products (New Name)": "Produk Perawatan Pribadi",
    "Air Freight & Logistics": "Pengiriman Udara & Logistik",
    "Construction & Engineering": "Konstruksi & Rekayasa",
    "Household Products": "Produk Rumah Tangga",
    "Leisure Products": "Produk Rekreasi",
    "Ecommerce System Schema": "Skema Sistem E-commerce",
    "Tobacco": "Tembakau",
    "Property & Casualty Insurance": "Asuransi Properti & Kecelakaan",
    "Reinsurance": "Reasuransi",
    "Diversified Banks": "Bank yang Diversifikasi",
    "Passenger Airlines (New name)": "Maskapai Penumpang",
    "Passenger Airlines": "Maskapai Penumpang"
}

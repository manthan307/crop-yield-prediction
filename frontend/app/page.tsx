"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { translations } from "@/lib/translation";
import { useState } from "react";

export default function Home() {
  const [crop, setCrop] = useState("");
  const [location, setLocation] = useState("");
  const [soilType, setSoilType] = useState(""); // Add soilType state
  const [season, setSeason] = useState("");
  const [production, setProduction] = useState("");
  const [farmArea, setFarmArea] = useState("");
  const [fertilizer, setFertilizer] = useState("");
  const [pesticide, setPesticide] = useState("");
  const [year, setYear] = useState("");
  const [moisture, setMoisture] = useState("");
  const [nitrogen, setNitrogen] = useState("");
  const [potassium, setPotassium] = useState("");
  const [phosphorous, setPhosphorous] = useState("");
  const [results, setResults] = useState(false);
  const [prediction, setPrediction] = useState<{
    yield: string;
    fertilizer_suggestion?: string;
    tips?: string[];
  } | null>(null);
  const [lang, setLang] = useState<"en" | "hi" | "gu">("en"); // default English

  const t = translations[lang];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      crop,
      location,
      soilType, // Add soilType to payload
      season,
      production,
      farmArea,
      fertilizer,
      pesticide,
      year,
      moisture,
      nitrogen,
      potassium,
      phosphorous,
    };
    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setPrediction({
        yield: data.yield ?? "N/A",
        fertilizer_suggestion: data.fertilizer ?? "N/A",
        tips: data.tips ?? [],
      });
      setResults(true);
    } catch (err) {
      setPrediction({ yield: "Error", fertilizer_suggestion: "Error" });
      setResults(true);
    }
  };

  // Validation function
  const isFormValid =
    crop.trim() &&
    location.trim() &&
    soilType.trim() && // Validate soilType
    season.trim() &&
    production.trim() &&
    fertilizer.trim() &&
    pesticide.trim() &&
    farmArea.trim() &&
    year.trim() &&
    nitrogen.trim() &&
    potassium.trim() &&
    phosphorous.trim() &&
    !isNaN(Number(farmArea)) &&
    Number(farmArea) > 0 &&
    !isNaN(Number(year)) &&
    Number(year) > 1900;

  return (
    <section className="min-h-screen w-full flex items-center justify-center bg-[#181818] px-2">
      <Card className="w-full max-w-full md:max-w-md p-2 md:p-6">
        <CardHeader>
          <CardTitle>{t.crop_yield_prediction}</CardTitle>
          <CardAction>
            <Select
              value={lang}
              onValueChange={(value) => setLang(value as "en" | "hi" | "gu")}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select Language" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Language</SelectLabel>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="hi">Hindi</SelectItem>
                  <SelectItem value="gu">Gujarati</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </CardAction>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="crop">{t.crop}</Label>
                <Input
                  id="crop"
                  type="text"
                  placeholder={t.crop}
                  required
                  value={crop}
                  onChange={(e) => setCrop(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="location">{t.location}</Label>
                <Input
                  id="location"
                  type="text"
                  placeholder={t.location}
                  required
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                />
              </div>
              <div className="flex flex-col md:flex-row gap-4">
                <div className="grid gap-2">
                  <Label>{t.soilType}</Label>
                  <Select value={soilType} onValueChange={setSoilType}>
                    <SelectTrigger className="w-full md:w-[180px]">
                      <SelectValue placeholder={t.soilType} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectGroup>
                        <SelectLabel>{t.soilType}</SelectLabel>
                        <SelectItem value="Loamy">Loamy Soil</SelectItem>
                        <SelectItem value="Red">Red Soil</SelectItem>
                        <SelectItem value="Sandy">Sandy Soil</SelectItem>
                        <SelectItem value="Clay">Clay Soil</SelectItem>
                        <SelectItem value="Slit">Slit Soil</SelectItem>
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label>{t.season}</Label>
                  <Select value={season} onValueChange={setSeason}>
                    <SelectTrigger className="w-full md:w-[180px]">
                      <SelectValue placeholder={t.season} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectGroup>
                        <SelectLabel>{t.season}</SelectLabel>
                        <SelectItem value="kharif">Kharif</SelectItem>
                        <SelectItem value="rabi">Rabi</SelectItem>
                        <SelectItem value="whole_year">Whole Year</SelectItem>
                        <SelectItem value="summer">Summer</SelectItem>
                        <SelectItem value="autumn">Autumn</SelectItem>
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="production">{t.production}</Label>
                <Input
                  id="production"
                  type="number"
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.production}
                  required
                  value={production}
                  onChange={(e) => setProduction(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="farm_area">{t.farmArea}</Label>
                <Input
                  id="farm_area"
                  type="number"
                  required
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.farmArea}
                  value={farmArea}
                  onChange={(e) => setFarmArea(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="Fertilizer">{t.fertilizer}</Label>
                <Input
                  id="Fertilizer"
                  type="number"
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.fertilizer}
                  required
                  value={fertilizer}
                  onChange={(e) => setFertilizer(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="Pesticide">{t.pesticide}</Label>
                <Input
                  id="Pesticide"
                  type="number"
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.pesticide}
                  required
                  value={pesticide}
                  onChange={(e) => setPesticide(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="year">{t.year}</Label>
                <Input
                  id="year"
                  type="number"
                  required
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.year}
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="moisture">{t.moisture}</Label>
                <Input
                  id="moisture"
                  type="number"
                  required
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.moisture}
                  value={moisture}
                  onChange={(e) => setMoisture(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="nitrogen">{t.nitrogen}</Label>
                <Input
                  id="nitrogen"
                  type="number"
                  required
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder={t.nitrogen}
                  value={nitrogen}
                  onChange={(e) => setNitrogen(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="potassium">{t.potassium}</Label>
                <Input
                  id="potassium"
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  type="number"
                  required
                  placeholder={t.potassium}
                  value={potassium}
                  onChange={(e) => setPotassium(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="phosphorous">{t.phosphorous}</Label>
                <Input
                  id="phosphorous"
                  className="[&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  type="number"
                  required
                  placeholder={t.phosphorous}
                  value={phosphorous}
                  onChange={(e) => setPhosphorous(e.target.value)}
                />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex-col gap-2">
          <Button
            type="submit"
            className="w-full"
            onClick={handleSubmit}
            disabled={!isFormValid}
          >
            {t.predictYield}
          </Button>
          {results && prediction ? (
            <div className="border border-green-600 rounded-md p-2 text-center text-green-600 w-full">
              <p>
                {t.predictedYield}: {prediction.yield} kg/ha
              </p>
              <p>
                {t.fertilizerSuggestion}: {prediction.fertilizer_suggestion}
              </p>
              <div className="mt-2 text-left">
                <h3 className="font-semibold">{t.tips}:</h3>
                {prediction.tips && prediction.tips.length > 0 ? (
                  <ul className="list-disc list-inside">
                    {prediction.tips.map((tip, index) => (
                      <li key={index}>{tip}</li>
                    ))}
                  </ul>
                ) : (
                  <p>{t.noTips}</p>
                )}
              </div>
            </div>
          ) : null}
        </CardFooter>
      </Card>
    </section>
  );
}

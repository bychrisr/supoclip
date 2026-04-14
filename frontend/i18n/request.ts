import { getRequestConfig } from "next-intl/server";

import { getMessages } from "../src/i18n/get-messages";
import { parseAppLocale } from "../src/i18n/locale";
import { intlLocaleByAppLocale } from "../src/i18n/config";

export default getRequestConfig(async ({ locale }) => {
  const appLocale = parseAppLocale(locale);
  const messages = await getMessages(appLocale);

  return {
    locale: intlLocaleByAppLocale[appLocale],
    messages,
    timeZone: "America/Sao_Paulo",
  };
});


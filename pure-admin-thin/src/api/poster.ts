import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export interface PosterDataList {
  douban_id: string;
  movie_name: string;
  image_url: string;
  name_id: string | null;
  create_time: Date;
  update_time: Date;
}

export interface DataListResult {
  code: number;
  message: string;
  data: Array<PosterDataList>;
  total: number;
}

/** 获取poster数据 */
export const getPosterData = (data?: object) => {
  console.log(baseUrlApi("poster"), "---------");
  return http.request<DataListResult>("post", baseUrlApi("data-list"), { data });
};

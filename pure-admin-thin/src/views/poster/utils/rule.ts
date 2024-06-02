export interface PageInfo {
  pageSize: number;
  currentPage: number;
}

export interface requestPosterDataListParams {
  doubanId: string;
  movieName: string;
  imageType?: Array<string>;
  pageInfo: PageInfo;
}

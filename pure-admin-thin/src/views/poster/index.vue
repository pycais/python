<template>
  <div>
    <div>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="movieName"
            placeholder="图片名称"
            clearable
            size="large"
        /></el-col>
        <el-col :span="6">
          <el-input
            v-model="doubanId"
            placeholder="豆瓣ID"
            clearable
            size="large"
        /></el-col>
        <el-col :span="6">
          <el-select
            v-model="imageType"
            multiple
            collapse-tags
            collapse-tags-tooltip
            :max-collapse-tags="5"
            placeholder="Select"
            size="large"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-input
            v-model="doubanId"
            placeholder="豆瓣ID"
            clearable
            size="large"
        /></el-col>
      </el-row>
    </div>

    <div class="search">
      <el-button type="danger" size="large" @click="searchData">搜索</el-button>
      <el-button type="success" size="large" @click="clearData"
        >清空搜索</el-button
      >
    </div>
    <!-- style="width: 100%; border: 1px solid black; border-color: black" -->
    <div style="min-height: 700px">
      <el-table
        :data="result"
        border
        type="selection"
        :reserve-selection="true"
        :row-key="row => row.id"
        v-show="loading || result.length > 0"
        empty-text="的额"
      >
        <el-table-column prop="douban_id" label="豆瓣ID" width="180" />
        <el-table-column prop="image_url" label="图片地址" />
        <el-table-column prop="movie_name" label="影视名称" />
        <el-table-column prop="create_time" label="创建时间">
          <el-select
            v-model="imageType"
            multiple
            collapse-tags
            collapse-tags-tooltip
            :max-collapse-tags="5"
            placeholder="Select"
            size="large"
          >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-table-column>
        <template #empty>
          <div v-if="!loading">暂无数据</div>
        </template>
      </el-table>
    </div>

    <div class="page">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 15, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="length"
        size="large"
        style="float: right; margin-top; 300px"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted, toRef, toRefs } from "vue";
import { requestPosterDataListParams, PageInfo } from "./utils/rule";
import { DataListResult, getPosterData, PosterDataList } from "@/api/poster";
defineOptions({
  name: "poster"
});

const params: requestPosterDataListParams = reactive({
  movieName: "",
  doubanId: "",
  imageType: [],
  pageInfo: { pageSize: 10, currentPage: 1 }
});
const { currentPage, pageSize } = toRefs(params.pageInfo);
const { movieName, doubanId, imageType } = toRefs(params);
const length = ref(0);
const loading = ref<boolean>(false);
const result = ref([]);

const handleSizeChange = (val: number) => {
  currentPage.value = 1;
  console.log(`${val} items per page`);
};
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`);
};

const options = [
  {
    value: "官方剧照",
    label: "官方剧照"
  },
  {
    value: "工作照",
    label: "工作照"
  },
  {
    value: "新闻图片",
    label: "新闻图片"
  },
  {
    value: "粉丝图片",
    label: "粉丝图片"
  },
  {
    value: "截图",
    label: "截图"
  }
];

function searchData() {
  if (currentPage.value === 1) {
    getPosterDataList(params);
  } else {
    currentPage.value = 1;
  }
}

function clearData() {
  movieName.value = "";
  doubanId.value = "";
  imageType.value = [];
}

const stopWatch = watch([currentPage, pageSize], (newValue, oldValue) => {
  getPosterDataList(params);

  // console.log("sum变化了", newValue, oldValue);

  if (newValue[0] >= 100) {
    stopWatch();
  }
});

onMounted(() => {
  getPosterDataList(params);
});
// const params<requestPosterDataListParams> = reactive({ "pageSize": 1 });

function getPosterDataList(
  params: requestPosterDataListParams
): Promise<DataListResult> {
  return new Promise<DataListResult>((resolve, reject) => {
    loading.value = true;
    getPosterData(params)
      .then(data => {
        if (data?.code === 0) {
          // return data.data;
          console.log(params, "--------params", data.data.length);
          length.value = data.total;
          // Object.assign(result, []);
          result.value = [];
          result.value = data.data;
          // if (data.data.length > 0) {
          // Object.assign(result, data.data);
          // }
          resolve(data);
        } else {
          reject(new Error(data?.message || "请求失败"));
        }
      })
      .catch(error => {
        reject(error);
      })
      .finally(() => {
        loading.value = false;
      });
  });
}

// onMounted(() => {return getPosterData()});
</script>

<style lang="scss" scoped>
.search {
  margin: 15px 0;
  float: right;
  // margin-left: 90%;
}

.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.demo-pagination-block + .demo-pagination-block {
  margin-top: 10px;
}
.demo-pagination-block .demonstration {
  margin-bottom: 16px;
}
</style>

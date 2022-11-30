const STATS_TAG = "Stats";
const STATS_API_ROOT = "counters/";

export const tags = [STATS_TAG];

export default (builder) => ({
  stats: builder.query({
    query: () => STATS_API_ROOT,
    providesTags: [STATS_TAG],
  }),
});
